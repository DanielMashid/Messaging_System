from django.urls import path
from . import views

urlpatterns = [
    path('', views.MessagingHandler.home_page),
    path('write-message', views.MessagingHandler.write_new_message), # write message
    path('get-messages', views.MessagingHandler.get_messages_from_specific_user), # Get all messages for a specific user
    path('get-unread-messages', views.MessagingHandler.get_all_unread_messages_from_specific_user), # Get all unread messages for a specific user
    path('read-message/<int:id>', views.MessagingHandler.get_message_by_id), # read message
    path('delete-message/<int:id>', views.MessagingHandler.delete_message_by_id), # delete message

]