from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Message

import requests

class MessagesHandlerTest(APITestCase):

    def setup(self):
        self.endpoint = "https://messaging-system-daniel.herokuapp.com/message/" 
        self.updateTables()
        self.authenticateUser()

    def authenticateUser(self):
        response = self.client.post(self.endpoint, {'username': 'firstUser', 'password': 'abcd1234'})
        self.firstUserToken = response.data['access']
        response = self.client.post(self.endpoint, {'username': 'secondUser', 'password': 'abcd1234'})
        self.secondUserToken = response.data['access']

    def updateTables(self):
        self.firstUser = User.objects.create_user(id=1, username='firstUser', password='abcd1234', email='firstUser@firstUser.com')
        self.secondUser = User.objects.create_user(id=2, username='secondUser', password='abcd1234', email='secondUser@secondUser.com')
                                               
        self.message1 = Message.objects.create(id='1', sender=self.firstUser, receiver=self.secondUser, subject='Test1',
                                          message_content='Hello')
        self.message2 = Message.objects.create(id='2', sender=self.secondUser, receiver=self.firstUser, subject='Test2',
                                          message_content='How are you?')
        self.message3 = Message.objects.create(id='3', sender=self.secondUser, receiver=self.firstUser, subject='Test3',
                                               message_content='test body')

    def testRequestWithoutUserToken(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})






# get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "Hello world"}) # HTTP Request
# # print(get_response.text) # print raw text response
# # print(get_response.status_code)

# # HTTP Request -> HTML      
# # REST API HTTP Request -> JSON
# # JavaScript Object Notation ~ Python Dict
# print(get_response.json())
# # print(get_response.status_code)
