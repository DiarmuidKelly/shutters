# from shutter_controller import ShutterController
from mock import MagicMock, patch
MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from main import compare_date, date_formatter, city
from datetime import datetime, date
from astral.sun import sun
from mock import MagicMock, patch


class TestClass:
    def test_one(self):
        datetime_1 = datetime.fromisoformat('2022-12-31T23:00:00')
        date_1 = date.fromisoformat('2023-01-01')
        tomorrow = sun(city.observer, date=date_1)
        assert compare_date(datetime_1, tomorrow['dawn'])
    
    def test_two(self):
        datetime_1 = datetime.fromisoformat('2022-12-31T12:00:00')
        date_1 = date.fromisoformat('2022-12-31')
        today = sun(city.observer, date=date_1)
        assert compare_date(datetime_1, today['dusk'])
   
    def test_three(self):
        datetime_1 = datetime.fromisoformat('2022-12-31T01:00:00')
        date_1 = date.fromisoformat('2022-12-31')
        today = sun(city.observer, date=date_1)
        assert compare_date(datetime_1, today['dawn'])