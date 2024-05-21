from django.urls import path
from .views import chat_view, user_chat_view, search_messages

app_name = 'chat'  # Define the namespace

urlpatterns = [
    path('', chat_view, name='chat'),
    path('search/', search_messages, name='search_messages'),
    path('<str:username>/', user_chat_view, name='user_chat'), 
]
