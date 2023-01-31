from time import sleep

from flask import Flask, current_app, request
from datetime import timedelta, datetime, date
from astral import LocationInfo
from astral.sun import sun
from threading import Thread, Event

from shutter_controller import ShutterController

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

time_format = "%d-%m-%Y %H:%M:%S"
city = LocationInfo("Berlin", "Germany", "Europe/Berlin")

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
    global next_event_action
    global next_event_time
    return {"data": [next_event_time.strftime("%Y-%m-%dT%H:%M"), next_event_action.__name__]}


@app.route('/open-time', methods=['POST'])
def set_open_time():
    global next_event_action
    global next_event_time
    print(request.json)
    if request.json['action'] == 'open':
        next_event_action = Action.open
    else:
        next_event_action = Action.close

    next_event_time = datetime.fromisoformat(request.json['datetime'])

    return {"data": [next_event_time.strftime("%Y-%m-%dT%H:%M"), next_event_action.__name__]}


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

def date_formatter(date_string):
    return datetime.fromisoformat(str(datetime.strptime(date_string, time_format))).timestamp()

def compare_date(date_1, date_2):
    return date_formatter(date_1.strftime(time_format)) < date_formatter(date_2.strftime(time_format))

def set_next_event():
    print("Setting next event")
    now = datetime.now()
    today = sun(city.observer, date=date.today())
    if compare_date(now, today['dawn']):
        return today['dawn'], Action.open
    if compare_date(now, today['dusk']):
        return today['dusk'], Action.close
    tomorrow_datetime = datetime.now() + timedelta(days=1)
    tomorrow = sun(city.observer, date=datetime.date(tomorrow_datetime))
    if compare_date(now, tomorrow['dawn']): 
        return tomorrow['sunrise'], Action.open

class MyThread(Thread):
    StopEvent = 0
    
    def __init__(self,args):
        Thread.__init__(self)
        self.sleep_event = Event()
        self.StopEvent = args
        global next_event_action
        global next_event_time
        try:
            next_event_time, next_event_action = set_next_event()
        except Exception as e:
            print(f"error {e}")
        print(next_event_time)

    def run(self):
        while True:
            self.sleep_event.clear()
            self.sleep_event.wait(5)
            Thread(target=self._run).start()

    def _run(self):
        global next_event_action
        global next_event_time
        print(next_event_time)
        if compare_date(next_event_time, datetime.now()):
            next_event_action()
            next_event_time, next_event_action = set_next_event()
next_event_action = Action.open
next_event_time = None

Stop = Event()
t = MyThread(Stop)
t.setDaemon(True)
t.start()
t.sleep_event.set()

application = app

if __name__ == "__main__":
    application.run(host="0.0.0.0")
