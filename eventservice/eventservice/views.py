import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from eventservice.serializers import UserSerializer
from eventservice.models import Event

def index(request):

    data = {
        "user": UserSerializer(request.user).data
    }

    return render(request, "eventservice/index.html", data)

@api_view(http_method_names=['POST'])
def registration(request):
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")

    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }

    if len(User.objects.filter(email=email))>0:
        answer["error"] = "Данный email уже зарегистрирован!"
        return Response(answer)

    if len(User.objects.filter(username=username))>0:
        answer["error"] = "Данный username уже зарегистрирован!"
        return Response(answer)

    user = User.objects.create_user(username=username, email=email, password=password )
    auth_login(request, user)

    answer["ok"] = 1
    return Response(answer)

@api_view(http_method_names=['POST'])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }

    user = authenticate(username=username, password=password)

    if user is not None:
        auth_login(request, user)
        answer["ok"] = 1
        return Response(answer)
    else:
        answer["error"] = "Пользователь с такими данными не найден :c"
        return Response(answer)

@api_view(http_method_names=['POST'])
def get_data(request):
    
    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }

    if not request.user.is_authenticated:
        answer["error"] = "Вам необходимо авторизироваться!"
        return Response(answer)

    events = Event.get(all=True, user=request.user)
    answer['ok'] = 1
    if events is None:
        answer['data'] = []
    else:
        answer['data'] = [e.serialize() for e in events]
    return Response(answer)

@api_view(http_method_names=['POST'])
def delete(request):
    
    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }
    
    if not request.user.is_authenticated:
        answer["error"] = "Вам необходимо авторизироваться!"
        return Response(answer)

    event_id = request.data.get("event_id")

    event = Event.get(id=event_id)

    if event is None:
        answer["error"] = "Событие с таким id не найдено!"
        return Response(answer)
    else:
        event.delete()
        answer["ok"] = 1
        answer['data'] = 'Событие успешно удалено!'
        return Response(answer)


@api_view(http_method_names=['POST'])
def create(request):
    
    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }

    if not request.user.is_authenticated:
        answer["error"] = "Вам необходимо авторизироваться!"
        return Response(answer)

    title = request.data.get("title")
    event_type = request.data.get("event_type")
    description = request.data.get("description")
    date_appointed = request.data.get("date_appointed")

    event = Event.create(user=request.user, title=title, event_type=event_type, description=description, date_appointed=date_appointed)

    answer["ok"] = 1
    answer['data'] = event.serialize()
    return Response(answer)

@api_view(http_method_names=['POST'])
def update(request):
    
    answer = {
        "ok": 0,
        "error": "",
        "data": ""
    }

    if not request.user.is_authenticated:
        answer["error"] = "Вам необходимо авторизироваться!"
        return Response(answer)

    event_id = request.data.get("event_id")

    event = Event.get(id=event_id, user=request.user)

    if event is None:
        answer["error"] = "Событие с таким id не найдено!"
        return Response(answer)
    else:
        event.update(**request.data)
        answer["ok"] = 1
        answer['data'] = 'Событие успешно обновлено!'
        return Response(answer)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
