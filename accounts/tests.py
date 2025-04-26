from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_login_view(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # should redirect after login
        self.assertTrue(response.url.startswith("/"))  # check if redirected
