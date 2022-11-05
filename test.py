from datetime import timedelta, datetime, date
from astral import LocationInfo
from astral.sun import sun
import threading


time_format = "%d-%m-%Y %H:%M:%S"
class Action():
    def __init__(self) -> None:
        pass
    
    def open():
        print("open")
    
    def close():
        print("open")


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
        if datetime.now().strftime(time_format) < today['dawn'].strftime(time_format):
            return today['dawn'].strftime(time_format), Action.open
        if datetime.now().strftime(time_format) < today['dusk'].strftime(time_format):
            return today['dusk'].strftime(time_format), Action.close
        tomorrow_datetime = datetime.now() + timedelta(days=1)
        tomorrow = sun(city.observer, date=datetime.date(tomorrow_datetime))
        if datetime.now().strftime(time_format) < tomorrow['dawn'].strftime(time_format):
            return tomorrow['dawn'].strftime(time_format), Action.open

    def run(self):
        while True:
            self.sleep_event.clear()
            self.sleep_event.wait(2)
            threading.Thread(target=self._run).start()

    def _run(self):
        if datetime.now().strftime(time_format) > self.next_event_time:
            self.next_event_action()
            self.next_event_time, self.next_event_action = self.set_next_event()

my_thread = MyThread()
my_thread.start()

while True:
    input("Hit ENTER to force execution\n")
    my_thread.sleep_event.set()
