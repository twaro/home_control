from django.db import models
from .smart_home import smart_home as controller
from time import sleep
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

    def open_blind(self):
        print(f"Dummy opening, {self.room_name}, {self.device_type}, {self.device_name}, {self.go_up_pin}")
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' opening...", logs_directory)
        # # GPIO.output(self.go_up_pin, 0)                                     # Uncomment on production
        # print(self.device_name, self.device_type, self.go_up_pin, 0)
        # for i in range(150):                                                 # Uncomment on production
        #     sleep(0.2)                                                       # Uncomment on production
        #     # if GPIO.input(self.go_up_pin):                                 # Uncomment on production
        #     #     break                                                      # Uncomment on production
        # print(self.device_name, self.device_type, self.go_up_pin, 1)
        # # GPIO.output(self.go_up_pin, 1)                                     # Uncomment on production
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' opened.", logs_directory)

    def close_blind(self):
        print(f"Dummy closing, {self.room_name}, {self.device_type}, {self.device_name}, {self.go_down_pin}")
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closing...", logs_directory)
        # GPIO.output(self.go_down_pin, 0)                                   # Uncomment on production
        # for i in range(150):                                               # Uncomment on production
        #     sleep(0.2)                                                     # Uncomment on production
            # if GPIO.input(self.go_down_pin):                               # Uncomment on production
            #     break                                                      # Uncomment on production
        print(self.device_name, self.device_type, self.go_down_pin, 1)
        # GPIO.output(self.go_down_pin, 1)                                   # Uncomment on production
        controller.log_to_file(f"[WebServer] Blind '{self.device_name}' in '{self.room_name}' closed.", logs_directory)

    def initialize_blind(self):
        for pin in self.go_up_pin, self.go_down_pin:
            controller.log_to_file(f"[WebServer] Blind '{self.device_name} in '{self.room_name}' initializing...", logs_directory)
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, 1)                                            # Uncomment on production
            # GPIO.setup(pin, GPIO.OUT)                                      # Uncomment on production
            # GPIO.output(pin, GPIO.HIGH)                                    # Uncomment on production
            print("Initialize blinds or all blinds stop")
            controller.log_to_file(f"[WebServer] Blind '{self.device_name} initialized.", logs_directory)

class Light(models.Model):
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
            # TODO Find how to initialize Light
            # GPIO.setup(xxxx, xxx)
            # GPIO.output(pin, 1)
            print("Initialize light")
            controller.log_to_file(f"[WebServer] Light '{self.device_name} in '{self.room_name}' initialized", logs_directory)