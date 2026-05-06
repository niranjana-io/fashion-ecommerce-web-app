from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update({
            'placeholder': '10-digit number',
            'class': 'form-control',
            'id': 'id_phone'
        })

    def save(self, commit=True):
        user = super().save(commit)
        phone = self.cleaned_data['phone']
        UserProfile.objects.create(user=user, phone=phone)
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Your Username", widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))

class CheckOutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Shipping Address")
