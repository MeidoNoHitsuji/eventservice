from rest_framework import serializers

class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    username = serializers.CharField(max_length=50)