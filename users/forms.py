from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from client.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm, ):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Введите ваш email'}))
