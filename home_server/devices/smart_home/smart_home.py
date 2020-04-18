import RPi.GPIO as GPIO                                                   # Uncomment on production
from datetime import datetime, timedelta
from time import sleep
from os import system, listdir, remove
import threading


class Blind:
    def __init__(self, device_name=None, room_name=None, go_up_pin=None, go_down_pin=None):
        self.device_name = device_name
        self.room_name = room_name
        self.go_up_pin = go_up_pin
        self.go_down_pin = go_down_pin

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.go_up_pin, GPIO.OUT)
        GPIO.setup(self.go_down_pin, GPIO.OUT)
        pass

    def open_blind(self):
        self.setup_gpio()
        # If blind is closing (0 on input) - stop closing
        if not GPIO.input(self.go_down_pin):
            GPIO.output(self.go_down_pin, 1)
            log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' closing aborted!",
                                   logs_directory)
        log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' opening...",
                               logs_directory)
        GPIO.output(self.go_up_pin, 0)
        for i in range(150):
            sleep(0.2)
            # Break when during opening CLOSE Button or STOP Button clicked
            if not GPIO.input(self.go_down_pin) or (GPIO.input(self.go_up_pin) and GPIO.input(self.go_down_pin)):
                GPIO.output(self.go_up_pin, 1)
                break
        else:
            GPIO.output(self.go_up_pin, 1)
            log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' opened.",
                                   logs_directory)
        print(f"open blind {self.device_name} in {self.room_name}")

    def close_blind(self):
        self.setup_gpio()
        # If blind is opening (0 on input) - stop opening
        if not GPIO.input(self.go_up_pin):
            GPIO.output(self.go_up_pin, 1)
            log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' opening aborted!",
                                   logs_directory)
        log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' closing...",
                               logs_directory)
        GPIO.output(self.go_down_pin, 0)
        for i in range(150):
            sleep(0.2)
            # Break when during closing OPEN Button or STOP Button clicked
            if not GPIO.input(self.go_up_pin) or (GPIO.input(self.go_up_pin) and GPIO.input(self.go_down_pin)):
                GPIO.output(self.go_down_pin, 1)
                break
        else:
            GPIO.output(self.go_down_pin, 1)
            log_to_file(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' closed.",
                                   logs_directory)
            print(f"[ManualButton] Blind '{self.device_name}' in '{self.room_name}' closed.")
        print(f"close blind {self.device_name} in {self.room_name}")

    def initialize_blind(self):
        self.setup_gpio()
        GPIO.output(self.go_up_pin, 1)
        GPIO.output(self.go_down_pin, 1)
        log_to_file(f"[ManualButton] Blind '{self.device_name} initialized.", logs_directory)
        print(f"initialize blind {self.device_name}")

    def stop_blind(self):
        self.setup_gpio()
        GPIO.output(self.go_up_pin, 1)
        GPIO.output(self.go_down_pin, 1)
        log_to_file(f"[ManualButton] Blind '{self.device_name} stopped.", logs_directory)
        print(f"stop blind {self.device_name}")



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


def log_to_file(log_message, log_location):
    with open(f"{log_location}{datetime.now().date()}.txt", "a+") as f:
        print(f"{datetime.now().isoformat(sep=' ', timespec='milliseconds')} | " +
              log_message, file=f)


def remove_old_logs(last_days_logging, logs_directory):
    list_of_days = [(datetime.now().date() - timedelta(days=day)).strftime('%Y-%m-%d')
                    for day in range(last_days_logging)]

    directory_files = listdir(logs_directory)
    directory_files = [file[:-4] for file in directory_files]

    files_to_delete = list(set(directory_files) - set(list_of_days))

    for file in files_to_delete:
        remove(f"{logs_directory}{file}.txt")


def system_restart():
    # system('sudo reboot')
    print(f"system_restart")


def system_shutdown():
    # system('sudo poweroff -f')
    print(f"system_shutdown")


def read_connected_devices():
    devices = []
    with open('connected_devices.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            devices.append(eval(line))
    return devices


if __name__ =="__main__":

    last_days_logging = 7
    logs_directory = "logs/"

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
        # Django writes to file all configured devices in admin, below command reads the devices from file
        devices = read_connected_devices()
        blinds = []
        for element in devices:
            if element['type'] == 'blind':
                blinds.append(Blind(room_name=element['room_name_id'], device_name=element['device_name'],
                                    go_up_pin=element['go_down_pin'], go_down_pin=element['go_up_pin']))

        # Removes logs older than last_days_logging. Checks between 3.00 and 3.03 AM
        if datetime.now().hour == 3 and datetime.now().minute < 3:
            remove_old_logs(last_days_logging, logs_directory)

        if ManualButtons["Rolety_UP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_UP"].is_pressed():
                log_to_file(f"[ManualButton] All blinds opening...", logs_directory)
                for element in blinds:
                    background_thread = threading.Thread(target=element.open_blind)
                    background_thread.start()

        if ManualButtons["Rolety_DOWN"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_DOWN"].is_pressed():
                log_to_file(f"[ManualButton] All blinds closing...", logs_directory)
                for element in blinds:
                    background_thread = threading.Thread(target=element.close_blind)
                    background_thread.start()

        if ManualButtons["Rolety_STOP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_STOP"].is_pressed():
                log_to_file(f"[ManualButton] All blinds stopping...", logs_directory)
                for element in blinds:
                    background_thread = threading.Thread(target=element.stop_blind)
                    background_thread.start()

        if ManualButtons["Emergency_STOP"].is_pressed():
            sleep(0.5)
            if ManualButtons["Emergency_STOP"].is_pressed():
                log_to_file(f"[ManualButton] Emergency blinds stopping...", logs_directory)
                for element in blinds:
                    background_thread = threading.Thread(target=element.stop_blind)
                    background_thread.start()

        if ManualButtons["Reboot"].is_pressed():
            sleep(0.5)
            if ManualButtons["Reboot"].is_pressed():
                log_to_file(f"[ManualButton] Restart system performing...", logs_directory)
                background_thread = threading.Thread(target=system_restart)
                background_thread.start()

        if ManualButtons["Shutdown"].is_pressed():
            sleep(0.5)
            if ManualButtons["Shutdown"].is_pressed():
                log_to_file(f"[ManualButton] Shutdown system performing...", logs_directory)
                background_thread = threading.Thread(target=system_shutdown)
                background_thread.start()
