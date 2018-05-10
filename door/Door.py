import RPi.GPIO as GPIO
import time


class Door:
    def __init__(self):
        self.port_led_no = 38
        self.port_door = 36
        self.port_led_yes = 40

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def openn(self, door_port, light_port_yes, light_port_no):
        self.toogle(light_port_no, False)
        self.toogle(light_port_yes, True)
        for i in range(0, 50):
            self.toogle(door_port, True)
            time.sleep(0.02)
            self.toogle(door_port, False)
            time.sleep(0.02)

    def closee(self, door_port, light_port_yes, light_port_no):
        self.toogle(light_port_no, True)
        self.toogle(door_port, False)
        self.toogle(light_port_yes, False)

    def toogle(self, port, on):
        GPIO.setup(port, GPIO.OUT)
        if on:
            GPIO.output(port, GPIO.HIGH)
        else:
            GPIO.output(port, GPIO.LOW)

    def open_door(self):
        self.openn(self.port_door, self.port_led_yes, self.port_led_no)

    def close_door(self):
        self.closee(self.port_door, self.port_led_yes, self.port_led_no)


def test():
    open_door()
    time.sleep(3)
    close_door()
