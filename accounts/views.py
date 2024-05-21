from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            """
                FLAW 4: A02:2021-Cryptographic Failures
                Password saved in db as is and not encrypted   
                Fix commented under user.password
                It hashes the password
            """
            user.password = form.cleaned_data['password']
            #user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        """
            FLAW 4: A02:2021-Cryptographic Failures
            Authenticate using plain text passwords instead of hashed.
            Fix commented under user
        """
        user = authenticate_user(username, password)
        #user = authenticate(request, username=username, password=password)  # Use Django's authentication system
        if user is not None:
            login(request, user)
            return redirect('chat:chat')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def authenticate_user(username, password):
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            return user
    except User.DoesNotExist:
        return None
    return None