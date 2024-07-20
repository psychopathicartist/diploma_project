from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from content.forms import StyleForMixin
from users.models import User


class UserRegisterForm(StyleForMixin, UserCreationForm):
    """
    Класс для отображения формы модели регистрации
    """

    class Meta:
        model = User
        fields = ('phone', 'nick_name', 'password1', 'password2')


class UserForm(StyleForMixin, UserChangeForm):
    """
    Класс для отображения формы модели пользователя
    """

    class Meta:
        model = User
        fields = ('nick_name', 'phone', 'town', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
