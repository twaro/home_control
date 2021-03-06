import threading
import pytz
from time import sleep
from datetime import datetime
from os import environ, system
import django

environ.setdefault('DJANGO_SETTINGS_MODULE', 'home_server.settings')
django.setup()
import devices.models
import RPi.GPIO as GPIO
import logger as logger
import sun_cycles


class ManualButton:
    def __init__(self, button_name, pin=None):
        self.button_name = button_name
        self.pin = pin

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        # Set safe state for button
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"initialize {self.button_name}")

    def is_pressed(self):
        if not GPIO.input(self.pin):
            return True
        else:
            return False


def system_restart():
    def restart():
        system('sudo reboot')
    background_thread = threading.Thread(target=restart)
    background_thread.start()


def system_shutdown():
    def shutdown():
        system('sudo poweroff -f')
    background_thread = threading.Thread(target=shutdown)
    background_thread.start()


if __name__ == "__main__":
    last_days_logging = 7

    ManualButtons = {"Rolety_UP": ManualButton(button_name="Rolety_UP", pin=18),
                     "Rolety_DOWN": ManualButton(button_name="Rolety_DOWN", pin=23),
                     "Rolety_STOP": ManualButton(button_name="Rolety_STOP", pin=24),
                     "Emergency_STOP": ManualButton(button_name="Emergency_STOP", pin=25),
                     "Reboot": ManualButton(button_name="Reboot", pin=8),
                     "Shutdown": ManualButton(button_name="Shutdown", pin=7)
                     }
    for button in ManualButtons.values():
        button.initialize()

    today_sunrise = sun_cycles.Sunrise()
    today_sunset = sun_cycles.Sunset()

    while True:
        # Checks between 3.00 and 3.03 AM
        if datetime.now().hour == 3 and datetime.now().minute < 3:
            logger.remove_old_logs(last_days_logging, logger.get_logs_directory())
            # Instantiate sunrise and sunset every day
            today_sunrise = sun_cycles.Sunrise()
            today_sunset = sun_cycles.Sunset()

        current_time = pytz.timezone("Europe/Warsaw").localize(datetime.now())
        # Sunrise
        if today_sunrise.period_on < current_time < today_sunrise.period_off:
            logger.log_to_file(f"[AutoSun] All blinds opening...", logger.get_logs_directory())
            today_sunrise.action()

        if today_sunrise.period_on < current_time < today_sunrise.period_off:
            today_sunrise.set_inactive()
        # Sunset
        if today_sunset.period_on < current_time < today_sunset.period_off:
            logger.log_to_file(f"[AutoSun] All blinds closing...", logger.get_logs_directory())
            today_sunset.action()

        if today_sunset.period_on < current_time < today_sunset.period_off:
            today_sunset.set_inactive()

        # Manual buttons
        if ManualButtons["Rolety_UP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_UP"].is_pressed():
                devices.models.open_all_blinds(source="but")
                logger.log_to_file(f"[ManualButton] All blinds opening...", logger.get_logs_directory())

        if ManualButtons["Rolety_DOWN"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_DOWN"].is_pressed():
                devices.models.close_all_blinds(source="but")
                logger.log_to_file(f"[ManualButton] All blinds closing...", logger.get_logs_directory())

        if ManualButtons["Rolety_STOP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_STOP"].is_pressed():
                devices.models.stop_all_blinds(source="but")
                logger.log_to_file(f"[ManualButton] All blinds stopping...", logger.get_logs_directory())

        if ManualButtons["Emergency_STOP"].is_pressed():
            sleep(0.5)
            if ManualButtons["Emergency_STOP"].is_pressed():
                devices.models.stop_all_blinds(source="but")
                logger.log_to_file(f"[ManualButton] All blinds stopping...", logger.get_logs_directory())

        if ManualButtons["Reboot"].is_pressed():
            sleep(0.5)
            if ManualButtons["Reboot"].is_pressed():
                logger.log_to_file(f"[ManualButton] Restart system performing...", logger.get_logs_directory())
                system_restart()

        if ManualButtons["Shutdown"].is_pressed():
            sleep(0.5)
            if ManualButtons["Shutdown"].is_pressed():
                logger.log_to_file(f"[ManualButton] Shutdown system performing...", logger.get_logs_directory())
                system_shutdown()
