from django.core.cache import cache
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from emerald_heart.middleware import set_request
from emerald_heart.models import User


class TestAdminPage(TestCase):
    fixtures = ["auth.json"]

    def setUp(self):
        admin_user = User.objects.get(username="admin")
        self.client.force_login(admin_user)
        self.request = RequestFactory()
        self.request.user = admin_user
        set_request(self.request)

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def test_get_index(self):
        """Can render the admin index page."""
        r = self.client.get(reverse_lazy("admin:index"))
        self.assertEqual(r.status_code, 200)
