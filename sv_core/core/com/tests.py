"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import get_hash


class ComTestCase(TestCase):
    def setUp(self):
        pass
        # evnt1 = Event.objects.create(event_type="evnttest", is_cached=True)
        # self.id1 = evnt1.id

    def test_get_hash(self):
        for rec in range(1000):
            self.assertGreaterEqual(64, get_hash(rec, 64))
            self.assertGreater(get_hash(rec, 64), 0)

