from time import sleep

from flask import Flask, current_app
from datetime import timedelta, datetime, date
from astral import LocationInfo
from astral.sun import sun
import threading

from shutter_controller import ShutterController

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

time_format = "%d-%m-%Y %H:%M:%S"
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
        if datetime.strptime(datetime.now().strftime(time_format), time_format) < datetime.strptime(today['sunrise'].strftime(time_format), time_format):
            return today['sunrise'].strftime(time_format), Action.open
        if datetime.strptime(datetime.now().strftime(time_format), time_format) < datetime.strptime(today['dusk'].strftime(time_format), time_format):
            return today['dusk'].strftime(time_format), Action.close
        tomorrow_datetime = datetime.now() + timedelta(days=1)
        tomorrow = sun(city.observer, date=datetime.date(tomorrow_datetime))
        if datetime.strptime(datetime.now().strftime(time_format), time_format) < datetime.strptime(tomorrow['dawn'].strftime(time_format), time_format):
            return tomorrow['sunrise'].strftime(time_format), Action.open

    def run(self):
        while True:
            self.sleep_event.clear()
            self.sleep_event.wait(60)
            threading.Thread(target=self._run).start()

    def _run(self):
        if datetime.strptime(datetime.now().strftime(time_format), time_format) > datetime.strptime(self.next_event_time, time_format):
            self.next_event_action()
            self.next_event_time, self.next_event_action = self.set_next_event()

my_thread = MyThread()
my_thread.start()
my_thread.sleep_event.set()

application = app

if __name__ == "__main__":
    application.run(host="0.0.0.0")
