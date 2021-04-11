from rest_framework.test import APITestCase
from .models import User
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
import json

class UserApiViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'admin', 'admin', 'admin')
        payload = api_settings.JWT_PAYLOAD_HANDLER(self.user)
        self.token = api_settings.JWT_ENCODE_HANDLER(payload)
        self.api_logout()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
    
    def api_logout(self):
        self.client.credentials()

    def test_create_user_with_authentication(self):
        self.api_authentication()

        url = reverse("user_api")
        kwargs = {
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, User.objects.count())

    def test_create_user_no_authentication(self):
        self.api_logout()

        url = reverse("user_api")
        kwargs = {
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(401, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_create_user_wrong_data(self):
        self.api_authentication()

        url = reverse("user_api")
        kwargs = {
            "username": "",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

        kwargs = {
            "username": "usuario1",
            "email": "",
            "password": "123456"
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

        kwargs = {
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": ""
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

        kwargs = {
            "username": "usuario1",
            "email": "usuario1@",
            "password": "123456"
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_update_user_with_authentication(self):
        self.api_authentication()

        initial_kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        new_kwargs = {
            "username": "usuario2",
            "email": "usuario2@gmail.com",
            "password": "1234567"
        }
        user = User.objects.create_user(**initial_kwargs)
        url = reverse("user_api", kwargs={'pk': user.id})
        response = self.client.put(url, new_kwargs)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, User.objects.count())
    
    def test_update_user_no_authentication(self):
        self.api_logout()

        initial_kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        new_kwargs = {
            "username": "usuario2",
            "email": "usuario2@gmail.com",
            "password": "1234567"
        }
        user = User.objects.create_user(**initial_kwargs)
        url = reverse("user_api", kwargs={'pk': user.id})
        response = self.client.put(url, new_kwargs)
        self.assertEqual(401, response.status_code)
        self.assertEqual(2, User.objects.count())

    def test_update_user_wrong_data(self):
        self.api_authentication()

        initial_kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }

        user = User.objects.create_user(**initial_kwargs)
        url = reverse("user_api", kwargs={'pk': user.id})

        new_kwargs = {
            "username": "",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        response = self.client.put(url, new_kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())

        new_kwargs = {
            "username": "usuario1",
            "email": "",
            "password": "123456"
        }
        response = self.client.put(url, new_kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())

        new_kwargs = {
            "username": "usuario2",
            "email": "usuario1@gmail.com",
            "password": ""
        }
        response = self.client.put(url, new_kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())

        new_kwargs = {
            "username": "usuario1",
            "email": "usuario1@",
            "password": "123456"
        }
        response = self.client.put(url, new_kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(2, User.objects.count())
    
    def test_update_user_does_not_exist(self):
        self.api_authentication()

        url = reverse("user_api", kwargs={'pk': 9999})

        kwargs = {
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "admin"
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(404, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_delete_user_with_authentication(self):
        self.api_authentication()

        kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        user = User.objects.create_user(**kwargs)

        url = reverse("user_api", kwargs={'pk': user.id})
        response = self.client.delete(url, kwargs)
        self.assertEqual(204, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_delete_user_no_authentication(self):
        self.api_logout()

        kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        user = User.objects.create_user(**kwargs)

        url = reverse("user_api", kwargs={'pk': user.id})
        response = self.client.delete(url, kwargs)
        self.assertEqual(401, response.status_code)
        self.assertEqual(2, User.objects.count())
    
    def test_delete_user_does_not_exist(self):
        self.api_authentication()

        url = reverse("user_api", kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(404, response.status_code)
        self.assertEqual(1, User.objects.count())

    def test_list_user_with_authentication(self):
        self.api_authentication()

        url = reverse("user_api")
        kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        User.objects.create_user(**kwargs)
        response = self.client.get(url)
        response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_json['count'], User.objects.count())

    def test_list_user_no_authentication(self):
        self.api_logout()

        url = reverse("user_api")
        kwargs = {
            "name": "usuario1",
            "last_name": "usuario1",
            "username": "usuario1",
            "email": "usuario1@gmail.com",
            "password": "123456"
        }
        User.objects.create_user(**kwargs)
        response = self.client.get(url)
        response_json = json.loads(response.content)
        self.assertEqual(401, response.status_code)
