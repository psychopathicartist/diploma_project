from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Content(models.Model):
    """
    Модель контента для публикации и чтения
    """

    heading = models.CharField(max_length=200, verbose_name='заголовок')
    description = models.CharField(max_length=500, verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='превью', **NULLABLE)
    created_at = models.DateField(auto_now_add=True, verbose_name='дата публикации')
    is_premium = models.BooleanField(default=False, verbose_name='премиум публикация')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.heading}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
