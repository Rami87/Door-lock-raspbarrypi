import json
import os
import time

LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "access_log.jsonl"
)


def log_event(event, method, identity=None):
    """Append one access-control event to the shared JSON-lines log.

    event: "access_granted" | "access_denied" | "door_open" | "door_close"
    method: "keypad" | "face" | "rfid"
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    entry = {
        "timestamp": time.time(),
        "event": event,
        "method": method,
        "identity": identity,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def read_events():
    if not os.path.exists(LOG_PATH):
        return []
    events = []
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events
