from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
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
            return redirect('chat')
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

    # Check if the url link user is the same one as in the session. If not goes back to chat and pritns error
    # if user != request.user:
    #     print("ERROR! STOP TRYING TO SEE OTHER PEOPELS MESSAGES")
    #     return redirect('chat:chat')  # Redirect to the chat view or show an error message

    # Fetch messages where the user is the receiver or sender
    received_messages = Message.objects.filter(receiver=user).order_by('timestamp')
    sent_messages = Message.objects.filter(sender=user).order_by('timestamp')

    return render(request, 'chat/user_chat.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'username': user.username,
        'current_user': request.user.username
    })