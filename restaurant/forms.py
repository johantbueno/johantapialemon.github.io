from django.forms import ModelForm
from django import forms
from .models import Booking, MenuItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"