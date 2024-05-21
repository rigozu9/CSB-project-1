from django import forms
from .models import Message
from accounts.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

    receiver = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
