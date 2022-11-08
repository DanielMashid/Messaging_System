from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    path('write-message', views.MessagingHandler.write_new_message),
    path('get-messages', views.MessagingHandler.get_message_by_id),
    path('get-unread-messages', views.MessagingHandler.get_all_unread_messages_from_specific_user),
    path('get-message-by-id', views.MessagingHandler.get_message_by_id),
    path('delete_message-by-id', views.MessagingHandler.delete_message_by_id)
]