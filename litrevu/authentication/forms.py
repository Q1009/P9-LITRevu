from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

#SF4SB6UJ375-Rt

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput, max_length=30)

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
    