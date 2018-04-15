from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Empl


class AccessManagementTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        user = User.objects.create_user(**self.credentials)
        empl = Empl(user=user, lang='LANGRUS')
        empl.save()

    def test_login_page(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

