from django.test import TestCase

from .models import Event


class EventTestCase(TestCase):
    def setUp(self):
        evnt1 = Event.objects.create(event_type="evnttest", is_cached=True)
        self.id1 = evnt1.id

    def test_event_property(self):
        evnt1 = Event.objects.get(id=self.id1)
        self.assertEqual(evnt1.event_type, 'EVNTTEST')
