from django import forms
from .models import Car,Bid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model=Car
        fields=["title","description","starting_price","image"]

class BidForm(forms.ModelForm):
    class Meta:
        model=Bid
        fields=["amount"]




