#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import time

reader = SimpleMFRC522.SimpleMFRC522()

while(True):
    try:
        id, text = reader.read()
        print(id)
        print(text)
        time.sleep(1)
    finally:
        GPIO.cleanup()
