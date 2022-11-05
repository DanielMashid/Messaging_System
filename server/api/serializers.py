from rest_framework import serializers
from .models import Message
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "receiver", "subject", "message_content", ""]
