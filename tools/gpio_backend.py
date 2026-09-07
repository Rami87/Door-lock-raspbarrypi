"""Picks a real GPIO backend on a Raspberry Pi, or a no-op mock everywhere
else (a laptop with no GPIO hardware), so the same code can run either way.

Door.py and keypad.py import GPIO from here instead of importing
RPi.GPIO directly, and check SIMULATED to switch their I/O to the console
when there's no real hardware to drive.
"""

try:
    import RPi.GPIO as GPIO

    SIMULATED = False
except (ImportError, RuntimeError):
    from tools import mock_gpio as GPIO

    SIMULATED = True
