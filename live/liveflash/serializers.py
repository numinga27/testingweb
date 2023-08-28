from rest_framework import serializers
from .models import (Events, LiveOfEvents, EventId, Tournament, HockeyLiveEvents,TournamentHockey)


class EventsSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = Events
        fields = ['event_id', 'start_time', 'start_utime', 'game_time', 'short_name_away',
                  'away_name', 'away_score_current', 'away_score_part_1', 'short_name_home',
                  'home_name', 'home_score_current', 'home_score_part_1', 'home_images', 'away_images']


class LiveOfEventsSerializer(serializers.ModelSerializer):
    # использование ранее созданного сериализатора для связанной модели
    events = EventsSerializer()

    class Meta:
        model = LiveOfEvents
        fields = '__all__'


class EventLiveIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventId
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    events = EventsSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'tournament_stage_type', 'tournament_imng',
                  'TOURNAMENT_TEMPLATE_ID', 'TOURNAMENT_IMAGE', 'events']



class HockeyLiveEventsSerializer(serializers.ModelSerializer):
    HOME_IMAGES = serializers.ListField(allow_null=True, required=False)
    AWAY_IMAGES = serializers.ListField(allow_null=True, required=False)
    HOME_SCORE_PART_3 = serializers.CharField(allow_null=True, required=False)
    AWAY_SCORE_PART_3 = serializers.CharField(allow_null=True, required=False)
    HOME_SCORE_PART_2 = serializers.CharField(allow_null=True, required=False)
    AWAY_SCORE_PART_2 = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images = representation.get('HOME_IMAGES', [])
        home_images_string = ''.join(home_images)
        representation['HOME_IMAGES'] = home_images_string

        away_images = representation.get('AWAY_IMAGES', [])
        away_images_string = ''.join(away_images)
        representation['AWAY_IMAGES'] = away_images_string

        return representation
    
    class Meta:
        model = HockeyLiveEvents
        fields = '__all__'

class TournamentHockeySerializer(serializers.ModelSerializer):
    events_hockey = HockeyLiveEventsSerializer(many=True)

    class Meta:
        model = TournamentHockey
        fields = ['id', 'name', 'tournament_stage_type', 'tournament_imng', 'TOURNAMENT_TEMPLATE_ID', 'TOURNAMENT_IMAGE', 'events_hockey']