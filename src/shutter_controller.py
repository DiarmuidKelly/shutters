from time import sleep
import RPi.GPIO as io


io.setmode(io.BCM)

class ShutterController:
    def __init__(self):
        self.down_pin = 15
        self.up_pin = 14
        self.up_pin_state = 1
        self.down_pin_state = 1

        self.open_time = None

        io.setup(self.down_pin, io.OUT, initial=self.down_pin_state)
        io.setup(self.up_pin, io.OUT, initial=self.up_pin_state)

    def change_direction(self):
        if self.up_pin_state == 1:
            print("Go Down")
            self.down()
        elif self.down_pin_state == 1:
            print("Go Up")
            self.up()
        self.__commit_state()

    def up(self):
        self.down_pin_state = 1
        self.__commit_state()
        sleep(0.1)
        self.up_pin_state = 0
        self.__commit_state()

    def down(self):
        self.up_pin_state = 1
        self.__commit_state()
        sleep(0.1)
        self.down_pin_state = 0
        self.__commit_state()

    def stop(self):
        self.up_pin_state = 1
        self.down_pin_state = 1
        self.__commit_state()

    def __commit_state(self):
        io.output(self.up_pin, self.up_pin_state)
        io.output(self.down_pin, self.down_pin_state)