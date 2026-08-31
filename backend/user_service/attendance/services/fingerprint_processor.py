from datetime import datetime
from django.db import transaction
from django.utils import timezone
from ..models import HardwareNode, FingerprintStamp, Attendance
from entities.models import TimetableEntrySchedule

def process_fingerprint_scan(device_name, data):
    """
    Process a fingerprint scan received from an MQTT device.

    Expected data:

    {
        "event_type": "fingerprint_scan",
        "fingerprint": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """

    fingerprint_id = data.get("fingerprint")
    timestamp = data.get("timestamp")

    if fingerprint_id is None or not timestamp:
        print("Incomplete fingerprint scan data")
        return

    # Identify the hardware node
    try:
        hardware_node = (
            HardwareNode.objects
            .select_related("set", "set__timetable")
            .get(
                name=device_name,
                is_active=True,
            )
        )
    except HardwareNode.DoesNotExist:
        print(
            f"Unknown or inactive hardware node: "
            f"{device_name}"
        )
        return

    # Get the timetable assigned to this device's Set
    student_set = hardware_node.set

    if student_set is None:
        print(
            f"No Set assigned to hardware node: "
            f"{device_name}"
        )
        return

    timetable = student_set.timetable

    if timetable is None:
        print(
            f"No timetable assigned to Set: "
            f"{student_set}"
        )
        return

    # Parse the timestamp
    try:
        scan_datetime = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        scan_datetime = timezone.localtime(scan_datetime)

    except (ValueError, TypeError):
        print(
            f"Invalid timestamp received from "
            f"{device_name}: {timestamp}"
        )
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
        print(
            f"No scheduled class found for "
            f"{student_set} at {scan_datetime}"
        )
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
        print(
            f"Fingerprint {fingerprint_id} is not "
            f"enrolled on {device_name}"
        )
        return

    user = fingerprint_stamp.user

    # The fingerprint exists on the device, but has not yet been assigned to a student.
    if user is None:
        print(
            f"Fingerprint {fingerprint_id} on "
            f"{device_name} has not been assigned "
            f"to a user"
        )
        return

    # Verify that the fingerprint's user actually
    # belongs to the Set served by this device.

    if user.set_id != student_set.id:
        print(
            f"User {user.id} does not belong to "
            f"Set {student_set.id}"
        )
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
        print(
            f"Attendance already exists for user "
            f"{user.id} for "
            f"{schedule.timetable_entry.course.code}"
        )
        return

    print(
        f"Attendance recorded: "
        f"user={user.id}, "
        f"course={schedule.timetable_entry.course.code}, "
        f"schedule={schedule.id}, "
        f"device={device_name}"
    )


def process_fingerprint_enrollment(device_name, data):
    """
    Process a fingerprint enrollment event received
    from an MQTT device.

    Expected data:

    {
        "event_type": "fingerprint_enrolled",
        "fingerprint": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """

    fingerprint_id = data.get("fingerprint")

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


def process_device_status(device_name, data):
    """
    Handle device status events.
    """
    pass


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