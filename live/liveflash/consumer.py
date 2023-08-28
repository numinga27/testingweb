from channels.generic.websocket import AsyncWebsocketConsumer
import json
import threading
import time
from django.db import transaction
from .models import Tournament, Events
from .serializers import TournamentSerializer, EventsSerializer
import requests
import schedule

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def send_data(self, data):
        await self.send(text_data=json.dumps(data))
        self.send_request()  # Вызов метода send_request для обновления данных

    async def start_scheduling(self):
        schedule.every(5).seconds.do(self.send_request)
        while True:
            schedule.run_pending()
            time.sleep(1)

    async def send_request(self):
        with transaction.atomic():
            Tournament.objects.all().delete()
            Events.objects.all().delete()

            url = "https://flashlive-sports.p.rapidapi.com/v1/events/live-list"
            headers = {
                'X-RapidAPI-Key': "c68d4d6ac2mshe98277d48f502dbp188062jsn10858273d528",
                'X-RapidAPI-Host': "flashlive-sports.p.rapidapi.com"
            }
            params = {
                'timezone': '-4',
                'sport_id': '1',
                'locale': 'en_INT'
            }

            response = requests.get(url, headers=headers, params=params)
            parsed_data = response.json()
            print(parsed_data)
            for item in parsed_data['DATA']:
                tournament = Tournament()
                tournament.name = item['NAME']
                tournament.tournament_stage_type = item['TOURNAMENT_STAGE_TYPE']
                tournament.tournament_imng = item['TOURNAMENT_IMAGE']
                tournament.TOURNAMENT_TEMPLATE_ID = item['TOURNAMENT_TEMPLATE_ID']
                tournament.save()

                for event in item['EVENTS']:
                    data = {
                        'event_id': event['EVENT_ID'],
                        'start_time': event['START_TIME'],
                        'start_utime': event['START_UTIME'],
                        'game_time': event['GAME_TIME'],
                         'short_name_away': event['SHORTNAME_AWAY'],
                        'away_name': event['AWAY_NAME'],
                        'away_score_current': event['AWAY_SCORE_CURRENT'],
                        'away_score_part_1': event['AWAY_SCORE_PART_1'],
                        'away_score_part_2': event.get('AWAY_SCORE_PART_2', ''),
                        'short_name_home': event['SHORTNAME_HOME'],
                        'home_name': event['HOME_NAME'],
                        'home_score_current': event['HOME_SCORE_CURRENT'],
                        'home_score_part_1': event['HOME_SCORE_PART_1'],
                        'home_score_part_2': event.get('HOME_SCORE_PART_2', ''),
                        'home_images': event.get('HOME_IMAGES'),
                        'away_images': event.get('AWAY_IMAGES'),
                    }
                    serializer = EventsSerializer(data=data)
                    if serializer.is_valid():
                        event_object = serializer.create(
                            serializer.validated_data)
                        tournament.events.add(event_object)
                    else:
                        print(serializer.errors)
