from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path(r'^ws/conference/(?P<room_name>[^/]+)/$', consumers.ConferenceConsumer.as_asgi()),
]