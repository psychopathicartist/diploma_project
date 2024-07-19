from django.contrib import admin

from content.models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Отображение полей модели контента в админке
    """

    list_display = ('id', 'heading', 'description', 'created_at', 'views_count', 'author', 'is_premium')
