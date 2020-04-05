from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Room, Blind, Light
from .smart_home import smart_home as controller
import os
# Create your views here.
def index(request):

    room_names = Room.objects.all()
    all_blinds = Blind.objects.all()
    all_lights = Light.objects.all()
    logs_directory = "devices/smart_home/logs/"

    with open(f"devices/smart_home/connected_devices.txt", "w") as f:
        for element in all_blinds.values():
            element["type"] = "blind"
            print(element, file=f)
        for element in all_lights.values():
            element["type"] = "light"
            print(element, file=f)

    # for element in rolets:
    #     print(element.values())
        # print(getattr(element, "room_name"), getattr(element, "device_type"),
        #       getattr(element, "device_name"))

    if request.POST:
        received_data = request.POST
        print(received_data)
        main_action = received_data.get('main_action')
        try:
            if "all_blinds_open" in main_action:
                controller.log_to_file(f"[WebServer] All blinds opening...", logs_directory)
                for blind in Blind.objects.all():
                    blind.open_blind()
                controller.log_to_file(f"[WebServer] All blinds opened.", logs_directory)
            elif "all_blinds_close" in main_action:
                controller.log_to_file(f"[WebServer] All blinds closing...", logs_directory)
                for blind in Blind.objects.all():
                    blind.close_blind()
                controller.log_to_file(f"[WebServer] All blinds closed...", logs_directory)
            elif "all_blinds_stop" in main_action:
                controller.log_to_file(f"[WebServer] All blinds stopping...", logs_directory)
                for blind in Blind.objects.all():
                    blind.initialize_blind()
                controller.log_to_file(f"[WebServer] All blinds stopped.", logs_directory)
            elif "emergency_stop" in main_action:
                controller.log_to_file(f"[WebServer] Emergency stop performing...", logs_directory)
                for blind in Blind.objects.all():
                    blind.initialize_blind()
                for light in Light.objects.all():
                    light.initialize_light()
                controller.log_to_file(f"[WebServer] Emergency stop performed.", logs_directory)
            elif "restart_system" in main_action:
                controller.log_to_file(f"[WebServer] Restart system performing...", logs_directory)
                controller.system_restart()
                controller.log_to_file(f"[WebServer] Restart system performed.", logs_directory)
            elif "shutdown_system" in main_action:
                controller.log_to_file(f"[WebServer] Shutdown system performing...", logs_directory)
                controller.system_shutdown()
                controller.log_to_file(f"[WebServer] Shutdown system performed.", logs_directory)
            else:
                pass
        except:
            return HttpResponse("")

    context = {'room_names': room_names}
    print(context)
    return render(request, 'devices/index.html', context)

def room(request, room_name):
    # room_names = Room.objects.all()
    #
    # context = {'room_names': room_names,
    #            'room_name': room_name,
    #            'blinds_in_room': Blind.objects.all().filter(room_name__exact=room_name),
    #            }
    # print(context)
    # return render(request, 'devices/room.html', context)
    room_names = Room.objects.all()
    if request.POST:
        received_data = request.POST
        device_type = received_data.get('device_type')
        print(f"received_data: {received_data}")
        try:
            if 'blind' in device_type:
                room_name = received_data.get('room_name')
                blind_name = received_data.get('blind_name')
                action = received_data.get('action')
                if 'open' in action:
                    print(f"opening blind {blind_name}")
                    Blind.objects.get(device_name=blind_name).open_blind()
                    # class method to open the blind( get Blind object by blind_name.open_blind
                elif 'close' in action:
                    print(f"closing blind {blind_name}")
                    Blind.objects.get(device_name=blind_name).close_blind()
                # print(f"room: {received_data.get('room_name')}, device_type: blind,"
                #       f" blind_name: {received_data.get('blind_name')}")
                else:
                    pass
        except:
            return HttpResponse("")
        try:
            if 'light' in device_type:
                room_name = received_data.get('room_name')
                light_name = received_data.get('light_name')
                action = received_data.get('action')
                if 'turn_on' in action:
                    print(f"turning ON light {light_name}")
                    Light.objects.get(device_name=light_name).turn_on_light()
                elif 'turn_off' in action:
                    print(f"turning off light {light_name}")
                    Light.objects.get(device_name=light_name).turn_off_light()
                else:
                    pass
        except:
            return HttpResponse("")

    context = {'room_names': room_names,
               'room_name': room_name,
               'blinds_in_room': Blind.objects.all().filter(room_name__exact=room_name),
               'lights_in_room': Light.objects.all().filter(room_name__exact=room_name),
               }
    print(context)
    return render(request, 'devices/room.html', context)


def device(request, room_name, device_name):
    return HttpResponse(f"Room {room_name}, device {device_name} view")

# kuchnia = Room.objects.get_or_create(room_name="KITCHEN")
# pokoj = Room.objects.get_or_create(room_name="SALON")
# lazienka = Room.objects.get_or_create(room_name="BATHROOM")
# sypialnia = Room.objects.get_or_create(room_name="ROOM2")
# korytarz = Room.objects.get_or_create(room_name="HALL")
