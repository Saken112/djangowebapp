from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=30)
    last_name = forms.CharField(label="Фамилия", max_length=30)
    email = forms.EmailField(label="Email")
    birth_date = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={'type': 'date'}))
    profile_image = forms.ImageField(label="Фото профиля", required=False)
    role = forms.ChoiceField(label="Роль", choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'profile_image',
            'username',
            'role',
            'password1',
            'password2',
        ]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)