from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение полей модели пользователя в админке
    """

    list_display = ('phone', 'password', 'nick_name', 'phone', 'town', 'is_active', 'is_premium')
