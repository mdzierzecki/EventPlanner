from django.test import TestCase
from .models import Event, Participant
from .forms import Event
from django.contrib.auth.models import User
import datetime


class EventModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Event.objects.create(title=title,
                             city=city,
                             street=street,
                             description=description,
                             contact_description=contact_description,
                             date=date,
                             time=time,
                             event_status=event_status,
                             facebook=facebook,
                             website=website,
                             author=self.user)

    def test_post_title(self):
        obj = Event.objects.get(pk=1)
        self.assertEqual(obj.title, title)
        self.assertEqual(obj.city, city)
        self.assertEqual(obj.street, street)
        self.assertEqual(obj.description, description)
        self.assertEqual(obj.contact_description, contact_description)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.time, time)
        self.assertEqual(obj.event_status, event_status)
        self.assertEqual(obj.facebook, facebook)
        self.assertEqual(obj.website, website)
        self.assertEqual(obj.author, self.user)


# class EventFormTestCase(TestCase):
#     def test_valid_form(self):


# test data
title = "Event: How to be productive?"
city = "Warsaw"
street = "ul. Aleje Jerozolimskie 27/22"
description = "Its a description of the event"
contact_description = "For contact visit out Facebook page or send email: contact@cotact.com"
date = datetime.date(2010, 1, 1)
time = datetime.time(19, 22)
event_status = 'Aktywne'
facebook = "https://www.facebook.com/BiTwarszawa/"
website = "https://github.com/"