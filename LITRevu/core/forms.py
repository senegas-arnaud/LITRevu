from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Ticket

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'author', 'description', 'image']