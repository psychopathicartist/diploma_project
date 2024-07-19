from django.test import TestCase, Client
from django.urls import reverse

from content.models import Content
from users.models import User


class PublicationViewTest(TestCase):
    """
    Тестирование работы с публикациями
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone='88888888888', password='123456', is_active=True)
        self.content = Content.objects.create(heading='Тест1', description='Описание теста1',
                                              author=self.user, is_premium=True)
        self.client.force_login(user=self.user)

    def test_create_content(self):
        """
        Тестирование создания публикации
        """

        url = reverse('content:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/content_form.html')
        data = {
            'heading': 'Тест2',
            'description': 'Описание теста2',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('content:list'))
        self.assertEqual(Content.objects.all().filter(author_id=self.user).first().description,
                         'Описание теста1')
        self.assertEqual(Content.objects.all().filter(author_id=self.user).count(), 2)

    def test_content_list(self):
        """
        Тестирование списка публикаций
        """

        url = reverse('content:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Content.objects.count(), 1)

    def test_update_content(self):
        """
        Тестирование обновления публикации
        """

        url = reverse('content:edit', args=[self.content.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {
            'heading': 'Тест1',
            'description': 'Новое описание теста',
        }
        response = self.client.post(url, data)
        self.content.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.content.description, 'Новое описание теста')

    def test_delete_content(self):
        """
        Тестирование удаления публикации
        """

        url = reverse('content:delete', args=[self.content.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.delete(url)
        self.assertEqual(Content.objects.count(), 0)

    def test_reader_content_list(self):
        """
        Тестирование страницы публикаций для чтения
        """

        url = reverse('content:reader_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
