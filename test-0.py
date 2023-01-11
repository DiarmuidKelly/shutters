from datetime import timedelta, datetime, date
from astral import LocationInfo
from astral.sun import sun
import threading

time_format = "%d-%m-%Y %H:%M:%S"
city = LocationInfo("Berlin", "Germany", "Europe/Berlin")

today = sun(city.observer, date=datetime(2022, 12, 31))
tomorrow = sun(city.observer, date=datetime(2023, 1, 1))

print(datetime.strptime(today['dusk'].strftime(time_format), time_format) < datetime.strptime(tomorrow['dawn'].strftime(time_format), time_format))
print(today['dusk'].strftime(time_format))

print(datetime.strptime(datetime.now().strftime(time_format), time_format))

print(tomorrow['dawn'].strftime(time_format))
