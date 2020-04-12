from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('devices/<slug:room_name>/', views.room, name="room"),
    path('devices/<slug:room_name>/<slug:device_name>/', views.device, name="device"),
]