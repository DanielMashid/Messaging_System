from api.models import Message
from api.serializers import  MessageSerializer
from api.serializers import MessageSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
class MessagingHandler():

    @api_view(['GET'])
    def home_page(request):
        return Response({"Welcome to Home Page !!"}, status=status.HTTP_200_OK)

    @api_view(['POST'])
    def write_new_message(request):
        current_user = request.user
        print("current_user--> ", current_user)
        serializer = MessageSerializer(data = request.data)
        print("data--> ",serializer)
        if serializer.is_valid():
            new_message = Message.objects.create(
                sender = request.data['sender'],
                receiver = request.data['receiver'],
                subject = request.data['subject'],
                message_content = request.data['message_content'],
            )
            new_message.save()
            return Response({"message": "The message was sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response("Could not send message. Error is : " + str(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def get_messages_for_specific_user(request):
        current_user = request.data['receiver']
        messages = Message.objects.filter(receiver = current_user)
        serializer = MessageSerializer(list(messages), many = True)
        messages.update(is_read = True)
        messages.update()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_all_unread_messages_for_specific_user(request):
        current_user = request.data['receiver']
        unread_messages = Message.objects.filter(receiver = current_user, is_read=False)
        if(not unread_messages.exists()):
                return Response("No new unread messages", status=status.HTTP_200_OK) 
        serializer = MessageSerializer(list(unread_messages), many=True)
        unread_messages.update(is_read = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_message_by_id(request):
        current_user_name = request.data['receiver']
        current_message_id = request.data['id']
        print("current_user_name = ", current_user_name)
        print("current_user_id = ", current_message_id)
        messages = Message.objects.filter(receiver = current_user_name) | Message.objects.filter(sender = current_user_name)
        print("messages = ", messages.values())
        try:
          unique_message = messages.get(id=current_message_id)
        except Message.DoesNotExist:
            return Response({"detail": "Could not find such message."}, status=status.HTTP_200_OK)
        if unique_message.receiver == current_message_id and not unique_message.is_read:
            unique_message.is_read = True
            unique_message.update()
        serializer = MessageSerializer(unique_message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET', 'POST'])
    def delete_message_by_id(request): 
        current_user_name = request.data['receiver']
        current_message_id = request.data['id']
        messages = Message.objects.filter(receiver = current_user_name)| Message.objects.filter(sender = current_user_name)
        try:
          unique_message_to_delete = messages.get(id=current_message_id)
        except Message.DoesNotExist:
            return Response({"detail": "Could not find message."}, status=status.HTTP_200_OK)
        unique_message_to_delete.delete()
        return Response({"detail": "Message deleted successfully"}, status=status.HTTP_200_OK)
