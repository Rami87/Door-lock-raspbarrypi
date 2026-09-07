import time

from tools.gpio_backend import GPIO, SIMULATED


class Keypad:
    def __init__(self):
        self.data = []
        self._sim_buffer = []

        if SIMULATED:
            print("[keypad] no RPi.GPIO found - type your PIN on the console instead")
            return

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.MATRIX = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ['*', 0, '#', 'D']
        ]

        self.ROW = [7, 11, 13, 15]
        self.COL = [12, 16, 18, 32]

        for j in range(4):
            GPIO.setup(self.COL[j], GPIO.OUT)
            GPIO.output(self.COL[j], 1)

        for i in range(4):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read(self):
        if SIMULATED:
            return self._read_simulated()

        try:
            val = None
            while (val is None):
                for j in range(4):
                    GPIO.output(self.COL[j], 0)

                    for i in range(4):
                        if GPIO.input(self.ROW[i]) == 0:
                            val = self.MATRIX[i][j]
                            while (GPIO.input(self.ROW[i]) == 0):
                                time.sleep(0.1)
                                pass
                    GPIO.output(self.COL[j], 1)
            return val
        except KeyboardInterrupt:
            GPIO.cleanup()

    def _read_simulated(self):
        if not self._sim_buffer:
            line = input("Simulated keypad - type a PIN and press Enter: ")
            self._sim_buffer = list(line.strip()) + ["#"]
        return self._sim_buffer.pop(0)

def test():
    keypad = Keypad()
    while True:
        print(keypad.read())


if __name__ == "__main__":
    test()
