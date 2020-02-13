from django.test import TestCase
from events.models import Event, Participant
from events.forms import EventAddForm
from django.contrib.auth.models import User
import datetime


class FormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
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
                             author=user)


class EventFormTestCase(FormTestCase):
    def test_valid_form(self):
        obj = Event.objects.get(pk=1)
        data = {'title': obj.title, 'city': obj.city, 'street': obj.street, 'description': obj.description,
                'date': obj.date, 'time': obj.time, 'event_status': obj.event_status, 'facebook': obj.facebook,
                'website': obj.website}
        form = EventAddForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('title'), obj.title)
        self.assertEqual(form.cleaned_data.get('city'), obj.city)
        self.assertEqual(form.cleaned_data.get('street'), obj.street)
        self.assertEqual(form.cleaned_data.get('description'), obj.description)
        self.assertEqual(form.cleaned_data.get('date'), obj.date)
        self.assertEqual(form.cleaned_data.get('time'), obj.time)
        self.assertEqual(form.cleaned_data.get('event_status'), obj.event_status)
        self.assertEqual(form.cleaned_data.get('facebook'), obj.facebook)
        self.assertEqual(form.cleaned_data.get('website'), obj.website)



