from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import connection
from .models import Message
from .forms import MessageForm

User = get_user_model()

@login_required
def chat_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('chat:chat')
    else:
        form = MessageForm()

    sent_messages = Message.objects.filter(sender=request.user).order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'form': form,
        'sent_messages': sent_messages,
        'username': request.user.username
    })

@login_required
def user_chat_view(request, username):
    # Fetch the user specified in the URL
    user = get_object_or_404(User, username=username)

    """
        FLAW 1:  A01:2021-Broken Access Control 
        Fix commented below this.
        We have to check if the user from URL is the same as request.user.
        Request user is the one whos logged in and he shouldnt be able to see other peoples messages.
    """
    # if user != request.user:
    #     print("ERROR! STOP TRYING TO SEE OTHER PEOPELS MESSAGES")
    #     return redirect('chat:chat')  # Redirect to the chat view or show an error message

    received_messages = Message.objects.filter(receiver=user).order_by('timestamp')
    sent_messages = Message.objects.filter(sender=user).order_by('timestamp')

    return render(request, 'chat/user_chat.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'username': user.username,
        'current_user': request.user.username
    })

@login_required
def search_messages(request):
    query = request.GET.get('query', '')
    user = request.user
    if query:
        with connection.cursor() as cursor:
            """
                FLAW 2:  A03:2021-Injection 
                Fix commented below the cursor.execute this.
                When you search with input (%' OR '1'='1' --) you get all the messages in the database.
                You have to use parameterized SQL queries. 
                %s is a placeholder in parameterized SQL queries
            """
            cursor.execute(f"SELECT * FROM chat_message WHERE (sender_id = {user.id} OR receiver_id = {user.id}) AND content LIKE '%{query}%'")
            #cursor.execute("SELECT * FROM chat_message WHERE (sender_id = %s OR receiver_id = %s) AND content LIKE %s", [user.id, user.id, f'%{query}%'])
            results = cursor.fetchall()
    else:
        results = []

    return render(request, 'chat/search.html', {'results': results, 'query': query})