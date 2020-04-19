from os import environ, system
import django
environ.setdefault('DJANGO_SETTINGS_MODULE', 'home_server.settings')
django.setup()
from devices.models import Blind

import RPi.GPIO as GPIO
from time import sleep
import threading
import logger as logger
from datetime import datetime

class ManualButton:
    def __init__(self, button_name, pin=None):
        self.button_name = button_name
        self.pin = pin

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        # Set safe state for button
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)            # Uncomment on production
        print(f"initialize {self.button_name}")

    def is_pressed(self):
        if not GPIO.input(self.pin):
            return True
        else:
            return False


def system_restart():
    system('sudo reboot')


def system_shutdown():
    system('sudo poweroff -f')


if __name__ =="__main__":

    last_days_logging = 7
    logs_directory = logger.get_logs_directory()

    ManualButtons = {"Rolety_UP":      ManualButton(button_name="Rolety_UP", pin=18),
                     "Rolety_DOWN":    ManualButton(button_name="Rolety_DOWN", pin=23),
                     "Rolety_STOP":    ManualButton(button_name="Rolety_STOP", pin=24),
                     "Emergency_STOP": ManualButton(button_name="Emergency_STOP", pin=25),
                     "Reboot":         ManualButton(button_name="Reboot", pin=8),
                     "Shutdown":       ManualButton(button_name="Shutdown", pin=7)
                     }
    for button in ManualButtons.values():
        button.initialize()

    # Main infinite loop
    while True:
        # Removes logs older than last_days_logging. Checks between 3.00 and 3.03 AM
        if datetime.now().hour == 3 and datetime.now().minute < 3:
            logger.remove_old_logs(last_days_logging, logs_directory)

        if ManualButtons["Rolety_UP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_UP"].is_pressed():
                for blind in Blind.objects.all():
                    background_thread = threading.Thread(target=blind.open_blind, args=["but"])
                    background_thread.start()
                logger.log_to_file(f"[ManualButton] All blinds opening...", logs_directory)

        if ManualButtons["Rolety_DOWN"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_DOWN"].is_pressed():
                for blind in Blind.objects.all():
                    background_thread = threading.Thread(target=blind.close_blind, args=["but"])
                    background_thread.start()
                logger.log_to_file(f"[ManualButton] All blinds closing...", logs_directory)

        if ManualButtons["Rolety_STOP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_STOP"].is_pressed():
                for blind in Blind.objects.all():
                    background_thread = threading.Thread(target=blind.stop_blind, args=["but"])
                    background_thread.start()
                logger.log_to_file(f"[ManualButton] All blinds stopping...", logs_directory)

        if ManualButtons["Emergency_STOP"].is_pressed():
            sleep(0.5)
            if ManualButtons["Emergency_STOP"].is_pressed():
                for blind in Blind.objects.all():
                    background_thread = threading.Thread(target=blind.stop_blind, args=["but"])
                    background_thread.start()
                logger.log_to_file(f"[ManualButton] Emergency blinds stopping...", logs_directory)

        if ManualButtons["Reboot"].is_pressed():
            sleep(0.5)
            if ManualButtons["Reboot"].is_pressed():
                logger.log_to_file(f"[ManualButton] Restart system performing...", logs_directory)
                background_thread = threading.Thread(target=system_restart, args=["but"])
                background_thread.start()

        if ManualButtons["Shutdown"].is_pressed():
            sleep(0.5)
            if ManualButtons["Shutdown"].is_pressed():
                logger.log_to_file(f"[ManualButton] Shutdown system performing...", logs_directory)
                background_thread = threading.Thread(target=system_shutdown, args=["but"])
                background_thread.start()
