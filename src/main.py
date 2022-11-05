from time import sleep

import RPi.GPIO as io
from flask import Flask, current_app
from datetime import timedelta, datetime, date
from astral import LocationInfo
from astral.sun import sun
import threading

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
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

shutters = ShutterController()
shutters.stop()

@app.route('/')
def index():
    return current_app.send_static_file('index.html')


@app.route('/down')
def down():
    shutters.down()
    return 'Going Down!'


@app.route('/up')
def up():
    shutters.up()
    return 'Going Up!'


@app.route('/stop')
def stop():
    shutters.stop()
    return 'Stopping!'


@app.route('/open-time', methods=['GET'])
def get_open_time():
    return {"data": [my_thread.next_event_time, my_thread.next_event_action.__name__]}


@app.route('/open-time', methods=['POST'])
def set_open_time():
    if shutters.open_time is None:
        return 'unset'
    else:
        return shutters.open_time

class Action():
    def __init__(self) -> None:
        pass
    
    def open():
        shutters.up()
        sleep(35)
        shutters.stop()
    
    def close():
        shutters.down()
        sleep(18)
        shutters.stop()


city = LocationInfo("Berlin", "Germany", "Europe/Berlin")

class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sleep_event = threading.Event()
        self.daemon = True
        self.next_event_time, self.next_event_action = self.set_next_event()
        print(self.next_event_time)

    def set_next_event(self):
        print("Setting next event")
        today = sun(city.observer, date=date.today())
        if datetime.now().strftime('%H:%M:%S') < today['dawn'].strftime('%H:%M:%S'):
            return today['dawn'].strftime('%H:%M:%S'), Action.open
        if datetime.now().strftime('%H:%M:%S') < today['dusk'].strftime('%H:%M:%S'):
            return today['dusk'].strftime('%H:%M:%S'), Action.close
        
        tomorrow = sun(city.observer, date=datetime.date(tomorrow_datetime))
        if datetime.now().strftime('%H:%M:%S') < tomorrow['dawn'].strftime('%H:%M:%S'):
            return tomorrow['dawn'].strftime('%H:%M:%S'), Action.open

    def run(self):
        while True:
            self.sleep_event.clear()
            self.sleep_event.wait(2)
            threading.Thread(target=self._run).start()

    def _run(self):
        if datetime.now().strftime('%H:%M:%S') > self.next_event_time:
            self.next_event_action()
            self.next_event_time, self.next_event_action = self.set_next_event()

my_thread = MyThread()
my_thread.start()
my_thread.sleep_event.set()

def create_app():
    app.run(host="0.0.0.0")

if __name__ == "__main__":
    create_app()
