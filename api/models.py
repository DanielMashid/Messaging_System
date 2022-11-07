from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name="sender", help_text="The sender of the message.")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", help_text="The receiver of message.")
    subject = models.CharField(max_length=100, help_text="The subject of the message.")
    message_content = models.CharField(max_length=1000, help_text="The content of the message")
    creation_date = models.DateTimeField(auto_now_add=True , help_text="The date and time the message was sent")
    is_read = models.BooleanField(default=False, help_text="Was the message read by the receiver?")
    deleted_by_sender = models.BooleanField(default=False, help_text="Was the message deleted by the sender?")
    deleted_by_receiver = models.BooleanField(default=False, help_text="Was the message deleted by the receiver?")

    #TODO: update to string func of message.
    def __str__(self):
        return self.subject +"\n" + self.message_content
    
