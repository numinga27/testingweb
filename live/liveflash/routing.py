from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumer import YourConsumer

websockets = URLRouter([
    path(
        "ws/live-score/",YourConsumer,
        name="live-score",
    ),
])