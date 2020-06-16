from django.apps import AppConfig

class BackendService(AppConfig):
    name = 'backend'

    def ready(self):
        from backend import update
        update.start()
