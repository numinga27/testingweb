from django.urls import path
from liveflash.consumer import YourConsumer

websocket_urlpatterns = [
       path(r'ws/my_consumer/$', YourConsumer.as_asgi()),
   ]
   