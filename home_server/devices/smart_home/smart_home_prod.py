import RPi.GPIO as GPIO                                                   # Uncomment on production
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
            GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            GPIO.output(pin, 1)                                            # Uncomment on production
            GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
            # print(f"PIN {pin} initialized")                                  # Comment on production

    def open(self):
        log_to_file(f"Opening blind _{self.device_name}_ in _{self.room_name}_...")
        GPIO.output(self.go_up_pin, 0)                                     # Uncomment on production
        print(self.device_name, self._device_type, self.go_up_pin, 0)
        for i in range(150):
            sleep(0.2)
            if GPIO.input(self.go_up_pin):                                 # Uncomment on production
                break                                                      # Uncomment on production
        print(self.device_name, self._device_type, self.go_up_pin, 1)
        GPIO.output(self.go_up_pin, 1)                                     # Uncomment on production
        log_to_file(f"Blind _{self.device_name}_ in _{self.room_name}_ opened.")

    def close(self):
        log_to_file(f"Closing blind _{self.device_name}_ in _{self.room_name}_...")
        GPIO.output(self.go_down_pin, 0)                                   # Uncomment on production
        print(self.device_name, self._device_type, self.go_down_pin, 0)
        for i in range(150):
            sleep(0.2)
            if GPIO.input(self.go_down_pin):                               # Uncomment on production
                break                                                      # Uncomment on production
        print(self.device_name, self._device_type, self.go_down_pin, 1)
        GPIO.output(self.go_down_pin, 1)                                   # Uncomment on production
        log_to_file(f"Blind _{self.device_name}_ in _{self.room_name}_ closed.")



class ManualButton(Device):
    def __init__(self, button_name, _device_type="Manual_Button", room_name="", pin=None):
        self.pin = pin
        super().__init__(button_name, _device_type, room_name)

    def initialize(self):
        GPIO.setup(self.pin, GPIO.OUT)                                     # Uncomment on production
        GPIO.output(self.pin, 1)                                           # Uncomment on production
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)            # Uncomment on production
        print(f"PIN {self.pin} initialized")                                 # Comment on production

    def is_pressed(self):
            return not GPIO.input(self.pin)                                # Uncomment on production
            # return True                                                    # Comment on production


def log_to_file(log_message):
    with open(f"logs/{datetime.now().date()}.txt", "a") as f:
        print(f"{datetime.now().isoformat(sep=' ', timespec='milliseconds')} |  " +
              log_message, file=f)


def remove_old_logs(last_days_logging, logs_directory):
    list_of_days = [(datetime.now().date() - timedelta(days=day)).strftime('%Y-%m-%d')
                    for day in range(last_days_logging)]

    directory_files = listdir(logs_directory)
    directory_files = [file[:-4] for file in directory_files]

    files_to_delete = list(set(directory_files) - set(list_of_days))

    for file in files_to_delete:
        remove(f"{logs_directory}{file}.txt")


if __name__ =="__main__":


    last_days_logging = 20
    logs_directory = "/var/www/html/TwaroInteligent/logs/"

    Blinds = {"Roleta_1": Blind(device_name="Roleta_1", room_name="Salon", go_up_pin=2, go_down_pin=9),
              "Roleta_2": Blind(device_name="Roleta_2", room_name="Salon", go_up_pin=3, go_down_pin=11),
              "Roleta_3": Blind(device_name="Roleta_3", room_name="Salon", go_up_pin=4, go_down_pin=5),
              "Roleta_4": Blind(device_name="Roleta_4", room_name="Salon", go_up_pin=17, go_down_pin=6),
              "Roleta_5": Blind(device_name="Roleta", room_name="Korytarz", go_up_pin=27, go_down_pin=13),
              "Roleta_6": Blind(device_name="Roleta", room_name="Łazienka", go_up_pin=22, go_down_pin=19),
              "Roleta_7": Blind(device_name="Roleta", room_name="Kuchnia", go_up_pin=10, go_down_pin=26),
    }

    ManualButtons = {"Rolety_UP":      ManualButton(button_name="Rolety_UP", room_name="House", pin=18),
                     "Rolety_DOWN":    ManualButton(button_name="Rolety_DOWN", room_name="House", pin=23),
                     "Rolety_STOP":    ManualButton(button_name="Rolety_STOP", room_name="House", pin=24),
                     "Emergency_STOP": ManualButton(button_name="Emergency_STOP", room_name="House", pin=25),
                     "Reboot":         ManualButton(button_name="Reboot", room_name="House", pin=8),
                     "Shutdown":       ManualButton(button_name="Shutdown", room_name="House", pin=7)
                     }


    # Device.print_all(room="Kuchnia")
    # Device.print_all(room="all")

    GPIO.setmode(GPIO.BCM)                                                # Uncomment on production
    GPIO.setwarnings(False)                                               # Uncomment on production

    for device in Blinds.values():
        device.initialize()
    for device in ManualButtons.values():
        device.initialize()

    while True:                                                           # Uncomment on production
        # delete logs on the 1st of every month
        if datetime.now().day == 1:
            remove_old_logs(last_days_logging, logs_directory)

        if ManualButtons["Rolety_UP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_UP"].is_pressed():
                log_to_file("Button _UP_ pressed, opening blinds...")
                for device in Blinds.values():
                    device.open()
                log_to_file("Blinds opened.")
            else:
                log_to_file("Button _UP_ pressed shortly, no action!")

        if ManualButtons["Rolety_DOWN"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_DOWN"].is_pressed():
                log_to_file("Button _DOWN_ pressed, closing blinds...")
                for device in Blinds.values():
                    device.close()
                log_to_file("Blinds closed.")
            else:
                log_to_file("Button _DOWN_ pressed shortly, no action!")

        if ManualButtons["Rolety_STOP"].is_pressed():
            sleep(0.3)
            if ManualButtons["Rolety_STOP"].is_pressed():
                log_to_file("Button _STOP_ pressed!")
                for device in Blinds.values():
                    device.initialize()
            else:
                log_to_file("Button _STOP_ pressed shortly, no action!")

        if ManualButtons["Emergency_STOP"].is_pressed():
            sleep(0.5)
            if ManualButtons["Emergency_STOP"].is_pressed():
                log_to_file("Button _EMERGENCY_STOP_ pressed!")
                for device in Blinds.values():
                    device.initialize()
                # + inne device stop
            else:
                log_to_file("Button _EMERGENCY_STOP_ pressed shortly, no action!")

        if ManualButtons["Reboot"].is_pressed():
            sleep(0.5)
            if ManualButtons["Shutdown"].is_pressed():
                log_to_file("Button _REBOOT_ pressed!")
                system('sudo reboot')
            else:
                log_to_file("Button _REBOOT_ pressed shortly, no action!")

        if ManualButtons["Shutdown"].is_pressed():
            sleep(0.5)
            if ManualButtons["Shutdown"].is_pressed():
                log_to_file("Button _SHUTDOWN_ pressed!")
                system('sudo poweroff -f')
            else:
                log_to_file("Button _SHUTDOWN_ pressed shortly, no action!")
