from datetime import datetime

from rest_framework import serializers

from .models import Event 

class EventSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    event_type = serializers.CharField(max_length=50)
    date_appointed = serializers.DateTimeField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'event_type', 'date_appointed', 'date_created')
        read_only_fields = ('id', 'user', 'date_created')

    def create(self, validated_data):
        date_appointed = validated_data.get('date_appointed')
        if date_appointed and not isinstance(date_appointed, datetime):
            date_list = date_appointed.split(" ")
            date = date_list[0].split("-")
            time = date_list[1].split(":")
            validated_data['date_appointed'] = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
        event = Event.objects.create(**validated_data)
        event.save()
        return event

    def update(self, instance, validated_data):
        update_fields = []

        if 'date_appointed' in validated_data and not isinstance(validated_data['date_appointed'], datetime):
            date_list = validated_data['date_appointed'].split(" ")
            date = date_list[0].split("-")
            time = date_list[1].split(":")
            validated_data['date_appointed'] = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
        
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
                update_fields.append(key)

        if len(update_fields) > 0:
            instance.save(update_fields=update_fields)

        return instance