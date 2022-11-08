from api.models import Message
from api.serializers import WriteMessageSerializer, DisplayMessageSerializer, MessageSerializer
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, generics, permissions
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view


class MessagingHandler(): 
    # authentication
    authentication_classes = [authentication.BaseAuthentication]
    permissions_classes = [permissions.IsAuthenticated]
    
    # @csrf_exempt
    @api_view(['GET', 'POST'])
    def write_new_message(request):
        serializer = WriteMessageSerializer(data = request.data)
        if serializer.is_valid():
            new_message = Message.objects.create(
                sender = request.user,
                receiver = serializer.validated_data['receiver'],
                subject = serializer.validated_data['subject'],
                message_content = serializer.validated_data['message_content'],
                is_read = False,
                deleted_by_sender = False,
                deleted_by_receiver = False,
            )
            new_message.save()
            return Response({"message": "The message was sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @api_view(['GET', 'POST'])
    def get_messages_from_specific_user(request):
        messages = get_messages(request.data['User'])
        serializer = DisplayMessageSerializer(data = messages)
        if serializer.is_valid():
            messages.update(is_read = True)
            messages.save()
            return Response(serializer.data)
        else:
            return Response({"message": "serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @api_view(['GET', 'POST'])
    def get_all_unread_messages_from_specific_user(request):
        unread_messages = get_messages(request.data['User'], only_unread_messages=True)
        serializer = MessageSerializer(data = unread_messages)
        if serializer.is_valid():
            unread_messages.update(is_read = True)
            unread_messages.save()
            return Response(serializer.data)
        else:
            return Response({"message": "serializer is not valid"}, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['GET', 'POST'])
    def get_message_by_id(self, request, pk):
        messages = get_messages(request.data['User'], only_receiver=False)
        try:
          unique_message = messages.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if unique_message.receiver.id == request.data['User'] and not unique_message.is_read:
            unique_message.is_read = True
            unique_message.save()
        serializer = DisplayMessageSerializer(unique_message)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response({"message": "Something went wrong :("}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'POST'])
    def delete_message_by_id(self, request, pk):
        messages = get_messages(request.data['User'], only_receiver=False)
        try:
          unique_message_to_delete = messages.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if (unique_message_to_delete.sender.id == request.data['User']):
            unique_message_to_delete.deleted_by_sender = True
        else:
            unique_message_to_delete.deleted_by_receiver = True
        if unique_message_to_delete.deleted_by_receiver and unique_message_to_delete.deleted_by_sender:
            unique_message_to_delete.delete()
        unique_message_to_delete.save()
        return Response({"detail": "Message deleted successfully"}, status=status.HTTP_200_OK)


def get_messages(user, only_receiver=True, only_unread_messages=False):
        queryset = (Message.objects.filter(receiver = user).filter(deleted_by_receiver=False))
        if (only_unread_messages):
            queryset.filter(is_read=False)
        elif (not only_receiver):
            queryset = queryset |  Message.objects.filter(sender = user).filter(deleted_by_sender=False) 
        return queryset.order_by('creation_date')
