# Generated by Django 4.2.14 on 2024-07-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200, verbose_name='заголовок')),
                ('description', models.CharField(max_length=500, verbose_name='содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='превью')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='дата публикации')),
                ('is_premium', models.BooleanField(default=False, verbose_name='премиум публикация')),
                ('views_count', models.IntegerField(default=0, verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'публикации',
            },
        ),
    ]