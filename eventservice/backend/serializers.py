from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Event

class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ('id', 'username')   

class EventSerializer(serializers.Serializer):

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'event_type', 'date_appointed', 'date_created')
