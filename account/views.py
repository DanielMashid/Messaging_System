from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
# from account.models import Account
# from django.contrib.auth import  login, logout

@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
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

# @api_view(['POST'])
# def login_view(request):
#     username = request.data['username']
#     password = request.data['password']
#     # user = authenticate(request, username=username, password=password)
#     user = authenticate(username=username, password=password)
#     print("user = ", user)
#     if user is not None:
#         login(request, user)
#         return Response("You ("+username+") logged in successfully",status=status.HTTP_200_OK)
#     else:
#         return Response("You ("+username+") have not logged in successfully")

# def authenticate(username, password):
#     print("username =", username)
#     print("pass = ", password)
#     print("in autheneitcate")
#     try:
#         user = Account.objects.filter(username=username, password=password)
#         print("USERRRR= ", user)
#         if user is not None:
#             return user
#     except Account.DoesNotExist:
#         print("exception")
#         pass

#-------------------------------------------------------------------------------------------------
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.response import Response

# @api_view(['POST'])
# def login_username(request):
#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(request, username=username, password=password)
#     print("user = ", username)
#     if user is not None:
#         login(request, user)
#         return Response("You ("+username+") login to the system successfully.",status=status.HTTP_200_OK)
#     else:
#         return Response("You ("+username+") have not successfully logged in to the system")

# @api_view(['GET'])
# def logout_username(request):
#     user = request.user
#     print("user before --> ", user)
#     logout(request)
#     user = request.user
#     print("user after --> ", user)
#     return Response("You logout from the system!!", status=status.HTTP_200_OK)

# @api_view(['POST'])
# def register_username(request):
#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(request, username=username, password=password)
#     User.objects.create_user(username=username, password=password)
#     # login(request, user)
#     return Response("You ("+username+") registered successfully !!", status=status.HTTP_200_OK)




