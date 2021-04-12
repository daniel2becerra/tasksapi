from rest_framework.test import APITestCase
from .models import Task
from users.models import User
from rest_framework_jwt.settings import api_settings
from django.urls import reverse
import json

class TaskApiViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'admin', 'admin', 'admin')
        payload = api_settings.JWT_PAYLOAD_HANDLER(self.user)
        self.token = api_settings.JWT_ENCODE_HANDLER(payload)
        self.api_logout()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
    
    def api_logout(self):
        self.client.credentials()

    def test_create_task_with_authentication(self):
        self.api_authentication()

        url = reverse("task_api")
        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_create_task_no_authentication(self):
        self.api_logout()

        url = reverse("task_api")
        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(401, response.status_code)

    def test_create_task_wrong_data(self):
        self.api_authentication()

        url = reverse("task_api")
        kwargs = {
            "title": "",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "nueva tarea",
            "description": "",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "xxxxxx",
            "done": False,
            "user": self.user.id
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": ''
        }
        response = self.client.post(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())
    
    def test_update_task_with_authentication(self):
        self.api_authentication()

        initial_kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        new_kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": True,
            "user": self.user.id
        }
        task = Task.objects.create(**initial_kwargs)
        url = reverse("task_api", kwargs={'pk': task.id})
        response = self.client.put(url, new_kwargs)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())
    
    def test_update_task_no_authentication(self):
        self.api_logout()

        initial_kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        new_kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": True,
            "user": self.user.id
        }
        task = Task.objects.create(**initial_kwargs)
        url = reverse("task_api", kwargs={'pk': task.id})
        response = self.client.put(url, new_kwargs)
        self.assertEqual(401, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_update_task_wrong_data(self):
        self.api_authentication()

        initial_kwargs = {
            "title": "nueva tarea",
            "description": "Descripción de la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        task = Task.objects.create(**initial_kwargs)
        url = reverse("task_api", kwargs={'pk': task.id})

        kwargs = {
            "title": "",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "Nueva tarea",
            "description": "",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user.id
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "Nueva tarea",
            "description": "realizar la tarea",
            "datetime": "",
            "done": False,
            "user": self.user.id
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "Nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": ""
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

        kwargs = {
            "title": "Nueva tarea",
            "description": "realizar la tarea",
            "datetime": "xxxxxx",
            "done": False,
            "user": self.user.id
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_update_task_does_not_exist(self):
        self.api_authentication()

        url = reverse("task_api", kwargs={'pk': 9999})
        kwargs = {
            "title": "nueva tarea",
            "description": "Descripción de la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        response = self.client.put(url, kwargs)
        self.assertEqual(404, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

    def test_delete_task_with_authentication(self):
        self.api_authentication()

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        task = Task.objects.create(**kwargs)

        url = reverse("task_api", kwargs={'pk': task.id})
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Task.objects.filter(user=self.user).count())

    def test_delete_task_no_authentication(self):
        self.api_logout()

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        task = Task.objects.create(**kwargs)

        url = reverse("task_api", kwargs={'pk': task.id})
        response = self.client.delete(url)
        self.assertEqual(401, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_delete_task_does_not_exist(self):
        self.api_authentication()

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        task = Task.objects.create(**kwargs)

        url = reverse("task_api", kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(404, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_list_task_with_authentication(self):
        self.api_authentication()

        kwargs = {
            "title": "nueva tarea",
            "description": "realizar la tarea",
            "datetime": "2021-04-10 14:00:00",
            "done": False,
            "user": self.user
        }
        task = Task.objects.create(**kwargs)

        url = reverse("task_api")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Task.objects.filter(user=self.user).count())

    def test_list_task_no_authentication(self):
        self.api_logout()

        url = reverse("task_api")
        response = self.client.get(url)
        self.assertEqual(401, response.status_code)

    def test_list_task_search(self):
        self.api_authentication()

        title = 'Tarea para la busqueda'
        description = "descripcion de prueba para la busqueda"
        datetime = '2021-04-10 15:00:00'
        Task.objects.create(title=title, description=description, datetime=datetime, user=self.user)

        url = reverse("task_api")

        response = self.client.get(f'{url}?search={title}')
        response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_json['count'], 1)

        response = self.client.get(f'{url}?search=YYY')
        response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_json['count'], 0)

        response = self.client.get(f'{url}?search={description}')
        response_json = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_json['count'], 1)
