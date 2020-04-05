from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<slug:room_name>/', views.room, name="room"),
    path('<slug:room_name>/<slug:device_name>/', views.device, name="device"),
]