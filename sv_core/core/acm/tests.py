from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class AccessManagementTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        user = User.objects.create_user(**self.credentials)
        empl = Profile.objects.get(user=user)
        empl.location = "Moscow"
        empl.lang = 'LANGRUS'
        empl.skype = 'skype_acc'
        empl.save()

    def test_login_page(self):
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.context['user'].profile.skype, 'skype_acc')

