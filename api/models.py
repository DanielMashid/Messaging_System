from django.db import models
from messages_handler.settings import AUTH_USER_MODEL

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name="sent_messages", help_text="Sender of the message", on_delete=models.CASCADE)
    receiver = models.CharField(max_length=100, help_text="The receiver of message.")
    subject = models.CharField(max_length=100, help_text="The subject of the message.")
    message_content = models.CharField(max_length=1000, help_text="The content of the message")
    creation_date = models.DateTimeField(auto_now_add=True, help_text="The date and time the message was sent")
    is_read = models.BooleanField(default=False, help_text="Was the message read by the receiver?")


    def __str__(self):
        return self.sender

