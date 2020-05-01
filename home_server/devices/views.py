from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Room, Blind, Light
import logger as logger
import threading
import manual_buttons
import os


def index(request):

    room_names = Room.objects.all()


    context = {'room_names': room_names}

    if request.POST:
        received_data = request.POST
        main_action = received_data.get('main_action')
        try:
            if "all_blinds_open" in main_action:
                logger.log_to_file(f"[WebServer] All blinds opening...", logger.get_logs_directory())
                manual_buttons.open_all_blinds(source="web")
            elif "all_blinds_close" in main_action:
                logger.log_to_file(f"[WebServer] All blinds closing...", logger.get_logs_directory())
                manual_buttons.close_all_blinds(source="web")
            elif "all_blinds_stop" in main_action:
                logger.log_to_file(f"[WebServer] All blinds stopping...", logger.get_logs_directory())
                manual_buttons.stop_all_blinds(source="web")
            elif "emergency_stop" in main_action:
                logger.log_to_file(f"[WebServer] Emergency stop performing...", logger.get_logs_directory())
                manual_buttons.stop_all_blinds(source="web")
                for light in Light.objects.all():
                    light.initialize_light()
            elif "restart_system" in main_action:
                logger.log_to_file(f"[WebServer] Restart system performing...", logger.get_logs_directory())
                manual_buttons.system_restart()
            elif "shutdown_system" in main_action:
                logger.log_to_file(f"[WebServer] Shutdown system performing...", logger.get_logs_directory())
                manual_buttons.system_shutdown()
            else:
                pass
        except:
            return HttpResponse("")

    return render(request, 'devices/index.html', context)


def room(request, room_name):
    room_names = Room.objects.all()
    context = {'room_names': room_names,
               'room_name': room_name,
               'blinds_in_room': Blind.objects.all().filter(room_name__exact=room_name),
               'lights_in_room': Light.objects.all().filter(room_name__exact=room_name),
               }
    if request.POST:
        received_data = request.POST
        device_type = received_data.get('device_type')
        try:
            if 'blind' in device_type:
                blind_name = received_data.get('blind_name')
                action = received_data.get('action')
                if 'open' in action:
                    background_thread = threading.Thread(target=Blind.objects.get(device_name=blind_name).open_blind, args=["web"])
                    background_thread.start()
                elif 'close' in action:
                    background_thread = threading.Thread(target=Blind.objects.get(device_name=blind_name).close_blind, args=["web"])
                    background_thread.start()
                elif 'stop' in action:
                    background_thread = threading.Thread(target=Blind.objects.get(device_name=blind_name).stop_blind, args=["web"])
                    background_thread.start()
                else:
                    pass
                return render(request, 'devices/room.html', context)
        except:
            return HttpResponse("")
        try:
            if 'light' in device_type:
                light_name = received_data.get('light_name')
                action = received_data.get('action')
                if 'turn_on' in action:
                    Light.objects.get(device_name=light_name).turn_on_light()
                elif 'turn_off' in action:
                    Light.objects.get(device_name=light_name).turn_off_light()
                else:
                    pass
                return render(request, 'devices/room.html', context)
        except:
            return HttpResponse("")

    return render(request, 'devices/room.html', context)


def device(request, room_name, device_name):
    return HttpResponse(f"Room {room_name}, device {device_name} view")
