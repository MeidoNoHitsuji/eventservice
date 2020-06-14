from django.contrib.auth.models import User
from django.db import models

from datetime import datetime

from eventservice.enums import EventType

class Event(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=[(t, t.value) for t in EventType], default="") #По хорошему реализовать через отдельную таблицу, но тут так сделать
    description = models.TextField(default="")
    date_created = models.DateTimeField(auto_now=True)
    date_appointed = models.DateTimeField()
    alerted = models.BooleanField(default=False)
    
    @classmethod
    def create(self, user, title:str, event_type, date_appointed, description:str=""):
        if not isinstance(date_appointed, datetime):
            date_list = date_appointed.split(" ")
            date = date_list[0].split("-")
            time = date_list[1].split(":")
            date_appointed = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
        event = self(user = user, title = title, event_type = event_type, date_appointed = date_appointed , description = description)
        event.save()
        return event

    @classmethod
    def get(self, all=False, **kwargs):
        events = self.objects.filter(**kwargs)
        if len(events)>0:
            if all:
                return events
            else:
                return events[0]
        else:
            return None

    def update(self, **kwargs):
        update_fields = []
        if 'date_appointed' in kwargs and not isinstance(kwargs['date_appointed'], datetime):
            date_list = kwargs['date_appointed'].split(" ")
            date = date_list[0].split("-")
            time = date_list[1].split(":")
            kwargs['date_appointed'] = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                update_fields.append(key)

        if len(update_fields) > 0:
            self.save(update_fields=update_fields)

        return self

    def serialize(self) -> dict: #Можно быль создать класс Сериализвации, но так оптимальнее
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'date_appointed': self.date_appointed,
            'date_created': self.date_created
        }
