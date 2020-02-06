from django.test import TestCase
from .models import Event, Participant
from django.contrib.auth.models import User
import datetime


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Event.objects.create(title="Event: How to be productive?",
                             city="Warsaw",
                             street="ul. Aleje Jerozolimskie 27/22",
                             description="Its a description of the event",
                             contact_description="For contact visit out Facebook page or send email: contact@cotact.com",
                             date=datetime.date(2010, 1, 1),
                             time=datetime.time(19, 22),
                             event_status='Aktywne',
                             facebook="https://www.facebook.com/BiTwarszawa/",
                             website="https://github.com/",
                             author=self.user)

    def test_post_title(self):
        obj = Event.objects.get(pk=1)
        self.assertEqual(obj.title, "Event: How to be productive?")
        self.assertEqual(obj.city, "Warsaw")
        self.assertEqual(obj.street, "ul. Aleje Jerozolimskie 27/22")
        self.assertEqual(obj.description, "Its a description of the event")
        self.assertEqual(obj.contact_description, "For contact visit out Facebook page or send email: contact@cotact.com")
        self.assertEqual(obj.date, datetime.date(2010, 1, 1))
        self.assertEqual(obj.time, datetime.time(19, 22))
        self.assertEqual(obj.event_status, "Aktywne")
        self.assertEqual(obj.facebook, "https://www.facebook.com/BiTwarszawa/")
        self.assertEqual(obj.website, "https://github.com/")
        self.assertEqual(obj.author, self.user)
