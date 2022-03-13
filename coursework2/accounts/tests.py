import json
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
# Create your tests here.

class AccountTest(APITestCase):
    # access to user profile
    def test_userView(self):
        account = AccountFactory.create(pk=1)
        url = reverse('account:user_view',kwargs={'user_id':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test@gmail.com', response.content)

    # able to go into register page
    def test_registerPage(self):
        url=reverse('account:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quick and easy', response.content)