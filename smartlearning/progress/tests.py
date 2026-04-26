from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Progress


class ProgressAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create_user(username='u1', password='pass')
        Progress.objects.create(user=self.u1, xp=100)

    def test_leaderboard(self):
        resp = self.client.get('/progress/api/leaderboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)


class ProgressAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.u = User.objects.create_user(username='bob', password='pwd')

    def test_token_auth_and_create_progress(self):
        # obtain token
        resp = self.client.post('/api-token-auth/', {'username': 'bob', 'password': 'pwd'})
        self.assertEqual(resp.status_code, 200)
        token = resp.data.get('token')
        self.assertIsNotNone(token)

        # use token to create progress
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        resp2 = self.client.post('/progress/api/progress/', {'xp': 50})
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.data['xp'], 50)
