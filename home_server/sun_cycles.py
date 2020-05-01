import pytz
import manual_buttons

from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun


class SunObserver:

    def __init__(self):
        self.time = None
        self.active = False
        self.period_on = None
        self.period_off = None
        self.location = LocationInfo('wyry', 'slaskie', 'Europe/Warsaw', 50.135250, 18.894160)
        self.sun_info = sun(self.location.observer, date=datetime.today())

    def set_time(self, key):
        return self.sun_info[key].replace(tzinfo=timezone.utc).astimezone(tz=None)

    def action(self):
        if not self.active:
            self.active = True
            print("Set true")

    def set_inactive(self):
        self.active = False


class Sunrise(SunObserver):

    def __init__(self):
        super().__init__()
        self.time = self.set_time("sunrise")
        self.period_on = self.time - timedelta(minutes=3)
        self.period_off = self.time + timedelta(minutes=3)

    def action(self):
        super().action()
        manual_buttons.open_all_blinds(source="sun")


class Sunset(SunObserver):

    def __init__(self):
        super().__init__()
        self.time = self.set_time("sunset")
        self.period_on = self.time - timedelta(minutes=3)
        self.period_off = self.time + timedelta(minutes=3)

    def action(self):
        super().action()
        manual_buttons.close_all_blinds(source="sun")


if __name__ == "__main__":
    # Instantiate at 3 AM
    wschod = Sunrise()
    zachod = Sunset()

    current_time = pytz.timezone("Europe/Warsaw").localize(datetime.now())

    if wschod.period_on < current_time < wschod.period_off:
        wschod.action()

    if wschod.period_on < current_time < wschod.period_off:
        wschod.set_inactive()

    if zachod.period_on < current_time < zachod.period_off:
        zachod.action()

    if zachod.period_on < current_time < zachod.period_off:
        zachod.set_inactive()
