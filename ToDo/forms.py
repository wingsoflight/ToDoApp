from django.contrib.auth.forms import UserCreationForm
from .models import AppUser

class SignupForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ("username", "password1", "password2")