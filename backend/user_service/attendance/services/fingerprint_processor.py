from datetime import datetime
from django.db import transaction
from django.utils import timezone
from ..models import HardwareNode, FingerprintStamp, Attendance
from entities.models import TimetableEntrySchedule
from mqtt.rabbitmq.producer import request_mqtt_publish

def process_fingerprint_scan(device_name, data):
    """
    Process a fingerprint scan received from an MQTT device.
    -to mark attendance

    Expected data:

    {
        "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "event_type": "fingerprint_scan",
        "fingerprint_id": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """

    fingerprint_id = data.get("fingerprint_id")
    timestamp = data.get("timestamp")
    event_id = data.get("event_id")
    event_type = data.get("event_type")

    print("Hello")
    print(device_name, fingerprint_id, timestamp, event_id, event_type)

    if fingerprint_id is None or not timestamp or not event_id or not event_type:
        message = "Incomplete fingerprint scan data"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    # Identifies the hardware node
    try:
        hardware_node = (
            HardwareNode.objects
            .select_related("set", "set__timetable")
            .get(name=device_name, is_active=True)
        )
    except HardwareNode.DoesNotExist:
        message = f"Unknown or inactive hardware node: {device_name}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    # Get the timetable assigned to this device's Set
    student_set = hardware_node.set

    if student_set is None:
        message = f"No Set assigned to hardware node: {device_name}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    timetable = student_set.timetable

    if timetable is None:
        message = f"No timetable assigned to Set: {student_set}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    # Parse the timestamp
    try:
        scan_datetime = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        scan_datetime = timezone.localtime(scan_datetime)

    except (ValueError, TypeError):
        message = f"Invalid timestamp received from {device_name}: {timestamp}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    scan_date = scan_datetime.date()
    scan_time = scan_datetime.time()

    # Find the scheduled class at this exact date and time.
    schedule = (
        TimetableEntrySchedule.objects
        .filter(
            timetable_entry__timetable=timetable,
            date=scan_date,
            timetable_entry__start_time__lte=scan_time,
            timetable_entry__end_time__gte=scan_time,
        )
        .select_related(
            "timetable_entry",
            "timetable_entry__course",
        )
        .first()
    )

    if schedule is None:
        message = f"No scheduled class found for {student_set} at {scan_datetime}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return
    
    # Resolve fingerprint -> user
    try:
        fingerprint_stamp = (
            FingerprintStamp.objects
            .select_related("user")
            .get(
                hardware_node=hardware_node,
                fingerprint_id=fingerprint_id,
            )
        )

    except FingerprintStamp.DoesNotExist:
        message = f"Fingerprint {fingerprint_id} is not enrolled on {device_name}"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    user = fingerprint_stamp.user

    # The fingerprint exists on the device, but has not yet been assigned to a student.
    if user is None:
        message = f"Fingerprint {fingerprint_id} on {device_name} has not been assigned to a user"
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    # Verify that the fingerprint's user actually
    # belongs to the Set served by this device.

    if user.set_id != student_set.id:
        message = (f"User {user.id} does not belong to "
                f"Set {student_set.id}")
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return

    # Create attendance
    with transaction.atomic():
        attendance, created = Attendance.objects.get_or_create(
            user=user,
            timetable_entry_schedule=schedule,
            defaults={
                "time_in": scan_time,
                "is_present": True,
            },
        )

    if not created:
        message = (
            f"Attendance already exists for user "
            f"{user.id} for "
            f"{schedule.timetable_entry.course.code}"
        )
        print(message)
        process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "ERROR",
                                   message)
        return
    message = (
        f"Attendance recorded: "
        f"user={user.id}, "
        f"course={schedule.timetable_entry.course.code}, "
        f"schedule={schedule.id}, "
        f"device={device_name}"
    )
    process_fingerprint_status(device_name,
                                   event_id,
                                   event_type,
                                   "OK",
                                   message)


def process_fingerprint_enrollment(device_name, data):
    """
    Process a fingerprint enrollment event received
    from an MQTT device.

    Expected data:

    {
        "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "event_type": "fingerprint_enrolled",
        "fingerprint_id": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """

    fingerprint_id = data.get("fingerprint_id")

    if fingerprint_id is None:
        print("Fingerprint enrollment has no fingerprint ID")
        return

    # Identify the hardware node
    try:
        hardware_node = HardwareNode.objects.get(
            name=device_name,
            is_active=True,
        )
    except HardwareNode.DoesNotExist:
        print(
            f"Unknown or inactive hardware node: "
            f"{device_name}"
        )
        return

    # Create the fingerprint stamp.
    # user remains NULL until the fingerprint is
    # assigned to a student.

    with transaction.atomic():

        fingerprint_stamp, created = (
            FingerprintStamp.objects.get_or_create(
                hardware_node=hardware_node,
                fingerprint_id=fingerprint_id,
            )
        )

    if created:
        print(
            f"Fingerprint {fingerprint_id} registered "
            f"on {device_name}"
        )
    else:
        print(
            f"Fingerprint {fingerprint_id} already "
            f"exists on {device_name}"
        )


def process_fingerprint_status(device_name, *data):
    """
    Return status to device
    {
        event_id: 387209u9u3209u0s393290,
        event_type: 
        status: OK; CREATED; ERROR
        message: FP 1 has been updated
    }
    """
    topic = f"attendance/device/{device_name}/status"

    event_id, event_type, status, message = data

    payload = {
        "event_id": event_id,
        "event_type": event_type,
        "status": status,
        "message": message
    }
    request_mqtt_publish(topic, payload)

def process_mqtt_message(device_name, data):
    """
    Entry point for MQTT messages.
    """

    event_type = data.get("event_type")

    if event_type == "fingerprint_scan":
        process_fingerprint_scan(
            device_name,
            data,
        )

    elif event_type == "fingerprint_enrolled":
        process_fingerprint_enrollment(
            device_name,
            data,
        )

    else:
        print(
            f"Unknown event type: {event_type}"
        )