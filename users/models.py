from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from content.models import NULLABLE


class User(AbstractUser):
    """
    Модель пользователя, переопределенная от AbstractUser,
    основным полем теперь является номер телефона (phone), а не username
    """

    username = None

    phone = PhoneNumberField(region='RU', verbose_name='номер телефона', unique=True)
    nick_name = models.CharField(max_length=200, verbose_name='никнейм', unique=True)
    town = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    is_premium = models.BooleanField(default=False, verbose_name='премиум пользователь')
    is_active = models.BooleanField(default=False, verbose_name='активный пользователь')
    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)
    payment_session_id = models.CharField(max_length=300, verbose_name='ID сессии оплаты', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.nick_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
