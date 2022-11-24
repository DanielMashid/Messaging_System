from api.models import Message
from api.serializers import  MessageSerializer
from api.serializers import MessageSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
class MessagingHandler():

    @api_view(['GET'])
    def home_page(request):
        print("in home page")
        return Response({"Welcome to Home Page !!"}, status=status.HTTP_200_OK)

    @api_view(['POST'])
    def write_new_message(request):
        current_user = request.user
        print("current_user--> ", current_user)
        serializer = MessageSerializer(data = request.data)
        print("data--> ",serializer)
        if serializer.is_valid():
            new_message = Message.objects.create(
                sender = current_user,
                receiver = request.data['receiver'],
                subject = request.data['subject'],
                message_content = request.data['message_content'],
            )
            new_message.save()
            return Response({"message": "The message was sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response("Could not send message. Error is : " + str(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def get_messages_from_specific_user(request):
        print("request = ",request.GET["user"])
        # user = request.GET["user"]
        current_user = request.user
        # print("User = ",user)
        messages = Message.objects.filter(receiver = current_user)
        serializer = MessageSerializer(list(messages), many = True)
        # if serializer.is_valid():
        #     messages.update(is_read = True)
        # messages.update()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response({"message": "serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    @api_view(['GET'])
    def get_all_unread_messages_from_specific_user(request):
        user = request.GET["user"]
        # print("user=", user)
        unread_messages = Message.objects.filter(receiver = user, is_read=False)
        # print(">>>Unread messages: ", unread_messages.values() )
        if(not unread_messages.exists()):
                return Response("No new unread messages", status=status.HTTP_200_OK) 
        serializer = MessageSerializer(list(unread_messages), many=True)
        # print("Serializer: ", serializer.data)
        # if serializer.is_valid():
        unread_messages.update(is_read = True)
        # unread_messages.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response({"message": "serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_message_by_id(request, id):
        print("in function get_message_by_id")
        user = request.GET["user"]
        print("user = ", user)
        messages = Message.objects.filter(receiver = user)| Message.objects.filter(sender = user)
        print("messages = ", messages.values())
        # messages = get_messages(request.data['User'], only_receiver=False)
        print("before se")
        try:
          unique_message = messages.get(id=id)
        except Message.DoesNotExist:
            return Response({"detail": "Could not find such message."}, status=status.HTTP_200_OK)
        if unique_message.receiver.id == user and not unique_message.is_read:
            unique_message.is_read = True
            unique_message.update()
        serializer = MessageSerializer(unique_message)
        # if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     return Response({"message": "Something went wrong :("}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'POST'])
    def delete_message_by_id(request, id): 
        # print("in function delete_message_by_id")
        user = request.GET["user"]
        messages = Message.objects.filter(receiver = user)| Message.objects.filter(sender = user)
        # print("messages --> ", messages)
        try:
          unique_message_to_delete = messages.get(id=id)
        except Message.DoesNotExist:
            return Response({"detail": "Could not find message."}, status=status.HTTP_200_OK)
        unique_message_to_delete.delete()
        return Response({"detail": "Message deleted successfully"}, status=status.HTTP_200_OK)
