from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet

from .consumer import YourConsumer

class UpdateDataViewSet(ViewSet):
    def update_data(self, request):
        data_consumer = YourConsumer()
        data_consumer.scope = {
            'type': 'websocket',
            'url_route': {
                'kwargs': {},
            },
            'headers': [],
        }
        data_consumer.connection_info = {
            'reply_channel': 'websocket.send',
        }
        data_consumer.connect()
        return HttpResponse("Data update started.")