from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name="sender", help_text="The sender of the message.")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", help_text="The receiver of message.")
    subject = models.CharField(max_length=180, help_text="The subject of the message.")
    message_content = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)

    #TODO: update to string func of message.
    def __str__(self):
        return self.subject +"\n" + self.message_content
    
