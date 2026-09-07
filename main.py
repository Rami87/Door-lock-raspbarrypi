import queue
import threading
import time

from checker.keypad.KeypadPassChecker import Keypad_pass_checker
from door.Door import Door
from tools.access_log import log_event

DOOR_OPEN_SECONDS = 3

door = Door()
grant_queue = queue.Queue()
stop_event = threading.Event()


def keypad_worker():
    checker = Keypad_pass_checker()
    while not stop_event.is_set():
        granted = checker.auth()
        log_event("access_granted" if granted else "access_denied", "keypad")
        if granted:
            grant_queue.put("keypad")


def face_worker():
    try:
        from checker.face.FaceChecker import Face_checker
    except ImportError as e:
        print(f"Face recognition disabled (missing dependency): {e}")
        return

    try:
        checker = Face_checker()
    except RuntimeError as e:
        print(f"Face recognition disabled: {e}")
        return

    while not stop_event.is_set():
        identity = checker.recognize()
        if identity is None:
            continue
        if identity == "unknown":
            log_event("access_denied", "face")
        else:
            log_event("access_granted", "face", identity=identity)
            grant_queue.put("face")


def main():
    workers = [
        threading.Thread(target=keypad_worker, daemon=True),
        threading.Thread(target=face_worker, daemon=True),
    ]
    for worker in workers:
        worker.start()

    try:
        while True:
            method = grant_queue.get()
            door.open_door()
            log_event("door_open", method)
            time.sleep(DOOR_OPEN_SECONDS)
            door.close_door()
            log_event("door_close", method)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        door.cleanup()


if __name__ == "__main__":
    main()
