from django.db import models
from .smart_home import smart_home as controller
from time import sleep
import RPi.GPIO as GPIO
# Create your models here.
logs_directory = "devices/smart_home/logs/"

class Room(models.Model):
    room_name = models.CharField(max_length=120, unique=True, primary_key=True)

    def __str__(self):
        return self.room_name


class Blind(models.Model):
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE)
    device_type = "blind"
    device_name = models.CharField(max_length=120, default="")
    go_up_pin = models.PositiveIntegerField()
    go_down_pin = models.PositiveIntegerField()

    def __str__(self):
        return self.device_name

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.go_up_pin, GPIO.OUT)
        GPIO.setup(self.go_down_pin, GPIO.OUT)

    def open_blind(self):
        self.setup_gpio()
        # If blind is closing (0 on input) - stop closing
        if not GPIO.input(self.go_down_pin):
            GPIO.output(self.go_down_pin, 1)
            controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closing aborted!",
                                   logs_directory)
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' opening...",
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
            controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' opened.", logs_directory)

    def close_blind(self):
        self.setup_gpio()
        # If blind is opening (0 on input) - stop opening
        if not GPIO.input(self.go_up_pin):
            GPIO.output(self.go_up_pin, 1)
            controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' opening aborted!",
                                   logs_directory)
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closing...",
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
            controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closed.", logs_directory)
            print(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closed.")

    def initialize_blind(self):
        self.setup_gpio()
        GPIO.output(self.go_up_pin, 1)
        GPIO.output(self.go_down_pin, 1)
        controller.log_to_file(f"[WebServer] Blind '{self.device_name} initialized.", logs_directory)

    def stop_blind(self):
        self.setup_gpio()
        GPIO.output(self.go_up_pin, 1)
        GPIO.output(self.go_down_pin, 1)
        controller.log_to_file(f"[WebServer] Blind '{self.device_name} stopped.", logs_directory)
        print("stopped")


class Light(models.Model): # TODO This Class is not finished
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE)
    device_type = "light"
    device_name = models.CharField(max_length=120, default="")
    on_pin = models.PositiveIntegerField()
    off_pin = models.PositiveIntegerField()

    def __str__(self):
        return self.device_name

    def turn_on_light(self):
        print(f"Dummy opening, {self.room_name}, {self.device_type}, {self.device_name}, {self.on_pin}")
        controller.log_to_file(f"[WebServer] Light '{self.device_name}' in '{self.room_name}' turning on...", logs_directory)
        controller.log_to_file(f"[WebServer] Light '{self.device_name}' in '{self.room_name}' turned on.", logs_directory)

    def turn_off_light(self):
        print(f"Dummy opening, {self.room_name}, {self.device_type}, {self.device_name}, {self.off_pin}")
        controller.log_to_file(f"[WebServer] Light '{self.device_name}' in '{self.room_name}' turning off...", logs_directory)
        controller.log_to_file(f"[WebServer] Light '{self.device_name}' in '{self.room_name}' turned off.", logs_directory)

    def initialize_light(self):
        for pin in self.on_pin, self.off_pin:
            controller.log_to_file(f"[WebServer] Light '{self.device_name} in '{self.room_name}' initializing...", logs_directory)
            # GPIO.setup(xxxx, xxx)
            # GPIO.output(pin, 1)
            print("Initialize light")
            controller.log_to_file(f"[WebServer] Light '{self.device_name} in '{self.room_name}' initialized", logs_directory)