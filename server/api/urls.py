from django.urls import path

from . import views
# from .views import api_home

urlpatterns = [
    path('', views.MessagingHandler.api_home), # localhost:8000/
    path('write_message', views.MessagingHandler.write_new_message),
    path('get_messages', views.MessagingHandler.get_messages),
    path('get_unread_messages', views.MessagingHandler.get_all_unread_messages_from_specific_user),
    path('get_message_by_id', views.MessagingHandler.get_message_by_id),
    path('delete_message_by_id', views.MessagingHandler.delete_message_by_id)
]