from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Create a new user account.
        """
        url = reverse('user-list')
        data = {'username': 'animesh0721', 'password': 'Animesh@123', 'email': 'animesh0721@gmail.com'}
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'animesh0721')
