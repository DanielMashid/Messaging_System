from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"   

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        message = Message(
                        sender = self.validated_data['sender'],
                        receiver = self.validated_data['receiver'],
                        subject = self.validated_data['subject'],
                        message_content = self.validated_data['message_content'],
                    )

        message.save()
        return message     
       
