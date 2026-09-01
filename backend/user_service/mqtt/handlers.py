import json
from attendance.services.fingerprint_processor import (
    process_fingerprint_scan,
    process_fingerprint_enrollment)

def mqtt_message_handler(topic, payload):
    """
    Possible Payload Samples
    {
        "state_type": "online",
        "timestamp": "2026-08-14T20:30:00Z"
    }
    {
        "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "event_type": "fingerprint_scan",
        "finger_id": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """
    try:
        data = json.loads(payload.decode("utf-8"))

    except UnicodeDecodeError:
        print(f"Could not decode payload from {topic}")
        return

    except json.JSONDecodeError:
        print(f"Invalid JSON received on {topic}")
        return

    topic_parts = topic.split("/")
    if len(topic_parts) != 4:
        print(f"Invalid topic structure: {topic}")
        return

    _, _, thing_name, message_type = topic_parts

    if message_type == "events":
        process_fingerprint_scan(
            device_name=thing_name,
            data=data,
        )

    elif message_type == "status":
        process_fingerprint_enrollment(
            device_name=thing_name,
            data=data,
        )

    else:
        print(f"Does not Subscribe/Receive from this topic: {message_type}")


def mqtt_event_handler(device_name, data):
    #device_name: unique thing_name from topic
    #data: payload message
    """
    {
        "event_type": "fingerprint_scan" | "fingerprint_enrolled",
        "fingerprint_id": 42,
        "timestamp": "2026-08-14T20:30:00Z"
    }
    """

    event_type = data.get("event_type")
    fingerprint_id = data.get("fingerprint_id")
    timestamp = data.get("timestamp")

    if (not event_type or event_type not in ["fingerprint_scan", "fingerprint_enrolled"]
        ):
        print("Invalid fingerprint event_type")
        return

    if (not fingerprint_id or not isinstance(fingerprint_id, int)):
        print("Invalid fingerprint ID")
        return

    if (not timestamp or not isinstance(timestamp, str)):
        print("Invalid timestamp")
        return
    
def mqtt_status_handler(device_name, data):
    process_device_status(device_name=device_name, data=data)