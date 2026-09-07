from checker.keypad.KeypadPassChecker import Keypad_pass_checker
from door.Door import Door
import time

DOOR_OPEN_SECONDS = 3

checker = Keypad_pass_checker()
door = Door()

try:
    while True:
        if checker.auth():
            door.open_door()
            time.sleep(DOOR_OPEN_SECONDS)
            door.close_door()
except KeyboardInterrupt:
    pass
finally:
    door.cleanup()
