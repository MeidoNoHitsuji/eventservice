from django.apps import AppConfig

class EventService(AppConfig):
    name = 'eventservice'

    def ready(self):
        from eventservice import update
        update.start()
