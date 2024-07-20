from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class UserTest(TestCase):
    """
    Тестирование работы с пользователями
    """

    def setUp(self):
        self.client = Client()

    def test_user_register(self):
        """
        Тест регистрации пользователя
        """

        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_register_form.html')
        data = {
            'phone': '+78008008000',
            'nick_name': 'Name',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(nick_name='Name').exists())

    def test_user_update(self):
        """
        Тест обновления пользователя
        """

        data = {
            'phone': '+78008008000',
            'nick_name': 'Name',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.client.post(reverse('users:register'), data)

        new_user = User.objects.all().filter(nick_name='Name').first()
        url = reverse('users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        data = {
            'phone': '+78008008000',
            'nick_name': 'Name1',
        }
        response = self.client.post(url, data)
        new_user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
