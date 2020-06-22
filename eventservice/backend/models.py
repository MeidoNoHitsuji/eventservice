from django.contrib.auth.models import User
from django.db import models

from datetime import datetime

from backend.enums import EventType

class Event(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    event_type = models.CharField(max_length=50, choices=[(t, t.value) for t in EventType], default="") #По хорошему реализовать через отдельную таблицу, но тут так сделать
    description = models.CharField(max_length=500, default="")
    date_created = models.DateTimeField(auto_now=True)
    date_appointed = models.DateTimeField()
    alerted = models.BooleanField(default=False)

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