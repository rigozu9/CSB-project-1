from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User

"""
    FLAW 3: A07:2021-Identification and Authentication Failures   
    Fixed class commented under the original one.
    No password repeat and added djangos own password validator
"""

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput,
#         validators=[validate_password]  # Add password validators
#     )
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username',)

#     def clean_password2(self):
#         cd = self.cleaned_data
#         password = cd.get('password')
#         password2 = cd.get('password2')
#         if password and password2 and password != password2:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return password2
