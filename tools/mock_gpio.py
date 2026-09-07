"""A drop-in stand-in for RPi.GPIO, used automatically off the Pi (no
hardware output happens; door/keypad code that goes through this switches
to console-based simulation instead). See tools/gpio_backend.py.
"""

BOARD = "BOARD"
BCM = "BCM"
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0
PUD_UP = "PUD_UP"
PUD_DOWN = "PUD_DOWN"


def setmode(mode):
    pass


def setwarnings(flag):
    pass


def setup(channel, direction, pull_up_down=None):
    pass


def output(channel, value):
    pass


def input(channel):
    return HIGH


def cleanup():
    pass
