from django.urls import path

from . import views
# from .views import api_home

urlpatterns = [
    path('', views.MessagingHandler.api_home),
     # localhost:8000/api/
]