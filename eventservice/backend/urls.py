from django.conf.urls import url
from django.urls import path

from backend import views

urlpatterns = [
    # url(r'^get_user$', views.get_user, name='get_user'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^get_data$', views.get_data, name='get_data'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^create$', views.create, name='create'),
    url(r'^update$', views.update, name='update'),
]