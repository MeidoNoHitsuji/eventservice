from django.conf.urls import url
from django.urls import path

from rest_framework.routers import SimpleRouter

from backend import views

router = SimpleRouter()
router.register(r'auth', views.AuthView)
router.register(r'event', views.EventView)

urlpatterns = router.urls