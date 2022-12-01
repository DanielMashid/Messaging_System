import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.hashers import check_password
# from account.models import Account
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

@api_view(['POST',])
def registration_view(request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)      

@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response("You logout from the system!!", status=status.HTTP_200_OK)        


# @api_view(['POST'])
# def login_view(request):
#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(request, username=username, password=password)
#     # user = authenticate(username=username, password=password)
#     print("user = ", user)
#     if user is not None:
#         login(request, user)
#         return Response("You ("+username+") logged in successfully",status=status.HTTP_200_OK)
#     else:
#         return Response("You ("+username+") have not logged in successfully")





