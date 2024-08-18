# chatbot/urls.py

from django.urls import path
from .views import chat

urlpatterns = [
    path("", chat, name="chat"),  # Maps the root URL to the chat view
]
