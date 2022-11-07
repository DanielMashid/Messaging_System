from api.models import Message
from api.serializers import WriteMessageSerializer, DisplayMessageSerializer, MessageSerializer
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, generics, permissions
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class MessagingHandler(APIView):
    # authentication
    authentication_classes = [authentication.SessionAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def api_home(request, *args, **kwargs):
        # request -> HttpRequest -> Django
        # print(dir(request))
        # request.body
        body = request.body # byte string of JSON data
        data = {}
        try:
            data = json.loads(body) # string of JSON data -> Python Dict
        except:
            pass    
        print(data)
        # data['headers'] = request.headers # request.META ->
        data['headers'] = dict(request.headers)
        data['content_type'] = request.content_type

        return JsonResponse({"message": "Hi there, this is your Django API response!!"})

    def write_new_message(self, request):
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
    
    # helper
    def get_messages(self, user, only_receiver=True, only_unread_messages=False):
        queryset = (Message.objects.filter(receiver = user).filter(deleted_by_receiver=False))
        if (only_unread_messages):
            queryset.filter(is_read=False)
        elif (not only_receiver):
            queryset = queryset |  Message.objects.filter(sender = user).filter(deleted_by_sender=False) 
        return queryset.order_by('creation_date')

    def get_messages_from_specific_user(self, request):
        messages = self.get_messages(request.user)
        serializer = DisplayMessageSerializer(data = messages)
        messages.update(is_read = True)
        messages.save()
        return Response(serializer.data)

    def get_all_unread_messages_from_specific_user(self, request):
          unread_messages = self.get_messages(request.user, only_unread_messages=True)     
          serializer = DisplayMessageSerializer(data = unread_messages)
          unread_messages.update(is_read = True)
          unread_messages.save()
          return Response(serializer.data)

    def get_message_by_id(self, request, pk):
        messages = self.get_messages(request.user, only_receiver=False)
        try:
          unique_message = messages.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if unique_message.receiver.id == request.user.id and not unique_message.is_read:
            unique_message.is_read = True
            unique_message.save()
        serializer = DisplayMessageSerializer(unique_message)
        return Response(serializer.data)

    def delete_message_by_id(self, request, pk):
        messages = self.get_messages(request.user, only_receiver=False)
        try:
          unique_message_to_delete = messages.get(pk=pk)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if (unique_message_to_delete.sender.id == request.user.id):
            unique_message_to_delete.deleted_by_sender = True
        else:
            unique_message_to_delete.deleted_by_receiver = True
        if unique_message_to_delete.deleted_by_receiver and unique_message_to_delete.deleted_by_sender:
            unique_message_to_delete.delete()
        unique_message_to_delete.save()
        return Response({"detail": "Message deleted successfully"}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    # queryset = Message.objects.all()
    filterset_fields = ['id', 'sender', 'receiver']
    
    def get_queryset(self):
        return Message.objects.all()

