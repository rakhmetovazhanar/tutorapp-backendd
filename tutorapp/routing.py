from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/conference/<str:room_name>/', consumers.ConferenceConsumer.as_asgi()),
]