import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from backend.models import Event
from backend.serializers import EventSerializer

class AuthView(viewsets.ViewSet):

    queryset = User.objects.all()

    @action(detail=False, methods=["POST"])
    def registration(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        answer = {
            "ok": 0,
            "error": "",
            "data": {}
        }

        if len(User.objects.filter(email=email))>0:
            answer["error"] = "Данный email уже зарегистрирован!"
            return Response(answer)

        if len(User.objects.filter(username=username))>0:
            answer["error"] = "Данный username уже зарегистрирован!"
            return Response(answer)

        user = User.objects.create_user(username=username, email=email, password=password )
        Token.objects.create(user=user)

        answer["ok"] = 1
        answer["data"].update({
            'id': user.id,
            'username': user.username,
            'token': user.auth_token.key
        })
        return Response(answer)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        answer = {
            "ok": 0,
            "error": "",
            "data": {}
        }

        user = authenticate(username=username, password=password)

        if user is not None:
            answer["ok"] = 1
            answer["data"].update({
                'id': user.id,
                'username': user.username,
                'token': user.auth_token.key
            })
            return Response(answer)
        else:
            answer["error"] = "Пользователь с такими данными не найден :c"
            return Response(answer)

class EventView(viewsets.ViewSet,
                generics.GenericAPIView,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def get_data(self, request):
    
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
            serializer = EventSerializer(events, many=True)
            answer['data'] = serializer.data
        return Response(answer)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)