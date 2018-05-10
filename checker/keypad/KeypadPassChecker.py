from keypad import Keypad
from tools import myfile


class Keypad_pass_checker:
    def auth(self):
        inputt = Input()
        checker = Checker()

        inputt.read()
        if checker.compare(inputt):
            print("access granted")
        else:
            print("sorry no")
        return checker.compare(inputt)


class Input:
    def __init__(self):
        self.keypad = Keypad()

    def read(self):
        self.trial = ""
        char = self.keypad.read()
        while(char != "#"):
            self.trial += str(char)
            print(self.trial)
            char = self.keypad.read()
        return self.trial

    def get_input(self):
        return self.trial


class Checker:
    def __init__(self):
        self.solution = myfile.readfile("checker/keypad/test")

    def compare(self, input):
        #print("solution " + self.solution.strip())
        #print("input " + input.get_input().strip())
        return self.solution.strip() == input.get_input().strip()
