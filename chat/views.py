from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from accounts.models import User

@login_required  # Ensure the user is logged in
def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
            return redirect('chat')
    
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/chat.html', {'messages': messages, 'username': request.user.username})
