from django.db import models
# from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.CharField(max_length=100, help_text="The sender of the message.")
    receiver = models.CharField(max_length=100, help_text="The receiver of message.")
    subject = models.CharField(max_length=100, help_text="The subject of the message.")
    message_content = models.CharField(max_length=1000, help_text="The content of the message")
    creation_date = models.DateTimeField(auto_now_add=True, help_text="The date and time the message was sent")
    is_read = models.BooleanField(default=False, help_text="Was the message read by the receiver?")
    

# class Account(models.Model):
#     email = models.EmailField(max_length=100, help_text="The email of the user.")
#     username = models.CharField(max_length=100, help_text="The user that connect.")
#     password = models.CharField(max_length=100, help_text="The first password of the user.")
#     password2 = models.CharField(max_length=100, help_text="The second password of the user.")
