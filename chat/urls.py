from django.urls import path
from .views import chat_view, user_chat_view

app_name = 'chat'  # Define the namespace

urlpatterns = [
    path('', chat_view, name='chat'),
    path('<str:username>/', user_chat_view, name='user_chat'),
]
