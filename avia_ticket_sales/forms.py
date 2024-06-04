from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class AuthUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'field__input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'field__input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'field__input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'field__input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'field__input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'field__input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'field__input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'field__input'}))
    is_receive_news = forms.BooleanField(label='Получать рассылку',
                                         widget=forms.CheckboxInput(attrs={'class': 'a_select'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_receive_news')
