from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class WriteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["receiver", "subject", "message_content"]

class DisplayMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender","receiver", "subject", "message_content", "is_read", "deleted_by_sender", "deleted_by_receiver"]

