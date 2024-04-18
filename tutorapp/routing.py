from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/conference/(?P<room_name>\w+)/$", consumers.ConferenceConsumer.as_asgi()),
]