from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AdminDashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123", is_staff=True)
        self.client.login(username="admin", password="admin123")

    def test_dashboard_view(self):
        response = self.client.get(reverse("admin_panel:dashboard"))
        self.assertEqual(response.status_code, 200)
