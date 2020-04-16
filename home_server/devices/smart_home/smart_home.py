# import RPi.GPIO as GPIO                                                   # Uncomment on production
from datetime import datetime, timedelta
from time import sleep
from os import system, listdir, remove


class Room:
    def __init__(self, room_name):
        self.room_name = room_name


class Device(Room):
    instances = []

    def __init__(self, device_name, _device_type, room_name):
        self.device_name = device_name
        self._device_type = _device_type
        super().__init__(room_name)
        self.__class__.instances.append(self)

    @classmethod
    def print_all(cls, room):
        for instance in cls.instances:
            if instance.room_name == room:
                print(f"Room {room} - {instance.__dict__}")
            if room.casefold() == "all":
                print(f"{instance.__dict__}")


class Light(Device):
    def __init__(self, device_name, _device_type="Light", room_name="", pin_on=None, pin_off=None):
        self.pin_on = pin_on
        self.pin_off = pin_off
        super().__init__(device_name, _device_type, room_name)


class Blind(Device):
    def __init__(self, device_name, _device_type="Blind", room_name="", go_up_pin=None, go_down_pin=None):
        self.go_up_pin = go_up_pin
        self.go_down_pin = go_down_pin
        super().__init__(device_name, _device_type, room_name)

    def initialize(self):
        for pin in self.go_up_pin, self.go_down_pin:
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, 1)                                            # Uncomment on production
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
            print(f"Room: {self.room_name}, {self._device_type}: {self.device_name}, "
                  f"PIN: {pin} - initialized")                                  # Comment on production

    def open(self):
        log_to_file(f"Opening blind _{self.device_name}_ in _{self.room_name}_...")
        # GPIO.output(self.go_up_pin, 0)                                     # Uncomment on production
        print(self.device_name, self._device_type, self.go_up_pin, 0)
        for i in range(150):
            sleep(0.2)
            # if GPIO.input(self.go_up_pin):                                 # Uncomment on production
            #     break                                                      # Uncomment on production
        print(self.device_name, self._device_type, self.go_up_pin, 1)
        # GPIO.output(self.go_up_pin, 1)                                     # Uncomment on production
        log_to_file(f"Blind _{self.device_name}_ in _{self.room_name}_ opened.")

    def close(self):
        log_to_file(f"Closing blind _{self.device_name}_ in _{self.room_name}_...")
        # GPIO.output(self.go_down_pin, 0)                                   # Uncomment on production
        print(self.device_name, self._device_type, self.go_down_pin, 0)
        for i in range(150):
            sleep(0.2)
            # if GPIO.input(self.go_down_pin):                               # Uncomment on production
            #     break                                                      # Uncomment on production
        print(self.device_name, self._device_type, self.go_down_pin, 1)
        # GPIO.output(self.go_down_pin, 1)                                   # Uncomment on production
        log_to_file(f"Blind _{self.device_name}_ in _{self.room_name}_ closed.")



class ManualButton:
    def __init__(self, button_name, pin=None):
        self.button_name = button_name
        self.pin = pin

    def initialize(self):
        # GPIO.setup(self.pin, GPIO.OUT)                                     # Uncomment on production
        # GPIO.output(self.pin, 1)                                           # Uncomment on production
        # GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)            # Uncomment on production
        print(f"PIN: {self.pin} - initialized")                             # Comment on production

    def is_pressed(self):
            # return not GPIO.input(self.pin)                                # Uncomment on production
            return True  # delete when GPIO imported                         # Comment on production

def open_all_blinds_from_button(room_name, device_name, go_up_pin):
    print(device_name)
    # blinds initialization
    # GPIO.setup(pin, GPIO.OUT)  # Uncomment on production
    # GPIO.output(pin, 1)                                            # Uncomment on production
    # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
    # GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
    log_to_file(f"[ManualButton] Blind '{device_name}' in '{room_name}' opening...", logs_directory)
    # GPIO.output(go_up_pin, 0)                                     # Uncomment on production
    # for i in range(150):                                           # Uncomment on production
    #     sleep(0.2)                                                   # Uncomment on production
        # if GPIO.input(go_up_pin):                                 # Uncomment on production
        #     break                                                      # Uncomment on production
    # GPIO.output(go_up_pin, 1)                                     # Uncomment on production
    log_to_file(f"[ManualButton] Blind '{device_name}' in '{room_name}' opened...", logs_directory)

def close_all_blinds_from_button(room_name, device_name, go_down_pin):
    print(device_name)
    # blinds initialization
    # GPIO.setup(pin, GPIO.OUT)  # Uncomment on production
    # GPIO.output(pin, 1)                                            # Uncomment on production
    # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
    # GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
    log_to_file(f"[ManualButton] Blind '{device_name}' in '{room_name}' closing...", logs_directory)
    # GPIO.output(go_down_pin, 0)                                     # Uncomment on production
    # for i in range(150):                                           # Uncomment on production
    #     sleep(0.2)                                                   # Uncomment on production
        # if GPIO.input(go_down_pin):                                 # Uncomment on production
        #     break                                                      # Uncomment on production
    # GPIO.output(go_down_pin, 1)                                     # Uncomment on production
    log_to_file(f"[ManualButton] Blind '{device_name}' in '{room_name}' closed...", logs_directory)

def initialize_all_blinds_from_button(go_up_pin, go_down_pin):
        for pin in go_up_pin, go_down_pin:
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, 1)                                            # Uncomment on production
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
            pass                                                             # Comment on production

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
    system('sudo reboot')


def system_shutdown():
    system('sudo poweroff -f')


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

    # Django writes to file all configured devices in admin, below command reads the devices from file
    devices = read_connected_devices()
    # Initialize all blinds pins
    # # GPIO.setmode(GPIO.BCM)                                                # Uncomment on production
    # # GPIO.setwarnings(False)                                               # Uncomment on production
    for element in devices:
        if element['type'] == 'blind':
            initialize_all_blinds_from_button(go_up_pin=element['go_up_pin'],
                                              go_down_pin=element['go_down_pin'])

    # Main infinite loop
    # # while True:                                                           # Uncomment on production
    # Removes logs older than last_days_logging. Checks between 3.00 and 3.03 AM
    if datetime.now().hour == 3 and datetime.now().minute < 3:
        remove_old_logs(last_days_logging, logs_directory)

    if ManualButtons["Rolety_UP"].is_pressed():
        sleep(0.3)
        if ManualButtons["Rolety_UP"].is_pressed():
            log_to_file(f"[ManualButton] All blinds opening...", logs_directory)
            for element in devices:
                if element['type'] == 'blind':
                    open_all_blinds_from_button(room_name=element['room_name_id'],
                                                device_name=element['device_name'],
                                                go_up_pin=element['go_up_pin'])
            log_to_file(f"[ManualButton] All blinds opened.", logs_directory)
        else:
            log_to_file("[ManualButton] 'Button UP' pressed shortly, no action!", logs_directory)

    if ManualButtons["Rolety_DOWN"].is_pressed():
        sleep(0.3)
        if ManualButtons["Rolety_DOWN"].is_pressed():
            log_to_file(f"[ManualButton] All blinds closing...", logs_directory)
            for element in devices:
                if element['type'] == 'blind':
                    close_all_blinds_from_button(room_name=element['room_name_id'],
                                                device_name=element['device_name'],
                                                go_down_pin=element['go_down_pin'])
            log_to_file(f"[ManualButton] All blinds closed.", logs_directory)
        else:
            log_to_file("[ManualButton] 'Button DOWN' pressed shortly, no action!", logs_directory)

    if ManualButtons["Rolety_STOP"].is_pressed():
        sleep(0.3)
        if ManualButtons["Rolety_STOP"].is_pressed():
            log_to_file(f"[ManualButton] All blinds initializing...", logs_directory)
            for element in devices:
                if element['type'] == 'blind':
                    initialize_all_blinds_from_button(go_up_pin=element['go_up_pin'],
                                                      go_down_pin=element['go_down_pin'])
            log_to_file(f"[ManualButton] All blinds initialized.", logs_directory)
        else:
            log_to_file("[ManualButton] 'Button DOWN'  pressed shortly, no action!", logs_directory)

    if ManualButtons["Emergency_STOP"].is_pressed():
        sleep(0.5)
        if ManualButtons["Emergency_STOP"].is_pressed():
            log_to_file(f"[ManualButton] Emergency blinds initializing...", logs_directory)
            for element in devices:
                if element['type'] == 'blind':
                    initialize_all_blinds_from_button(go_up_pin=element['go_up_pin'],
                                                      go_down_pin=element['go_down_pin'])
            log_to_file(f"[ManualButton] Emergency blinds initialized.", logs_directory)
        else:
            log_to_file("[ManualButton] 'Button EMERGENCY'  pressed shortly, no action!", logs_directory)

    if ManualButtons["Reboot"].is_pressed():
        sleep(0.5)
        if ManualButtons["Shutdown"].is_pressed():
            log_to_file(f"[ManualButton] Restart system performing...", logs_directory)
            system_restart()
        else:
            log_to_file("[ManualButton] Restart system performed...", logs_directory)

    if ManualButtons["Shutdown"].is_pressed():
        sleep(0.5)
        if ManualButtons["Shutdown"].is_pressed():
            log_to_file(f"[ManualButton] Shutdown system performing...", logs_directory)
            system_shutdown()
        else:
            log_to_file(f"[ManualButton] Shutdown system performed...", logs_directory)
