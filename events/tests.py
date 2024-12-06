from time import tzname

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime
import zoneinfo

from events.forms import EventForm


class EventsViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        self.client.force_login(self.user)

    def test_event_get_view(self):
        response = self.client.get(reverse('create_event'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_event.html')

    def test_event_create_view(self):
        response = self.client.post(reverse('create_event'), {'title': 'Test Event',
                                                              'datetime': '2023-08-01T12:00:00',
                                                              'description': 'Test Description',
                                                              'address': 'Москва, ул. Пушкина, д. 17',
                                                              'latitude': 55.755826,
                                                              'longitude': 37.6173})

        self.assertRedirects(response, reverse('event-create-success'))
        self.assertEqual(get_user_model().objects.get(username='testuser').event_set.count(), 1)

    def test_event_create_view_invalid_data(self):
        self.client.post(reverse('create_event'), {'title': 'Test Event',
                                                   'description': 'Test Description',
                                                   'address': 'Москва, ул. Пушкина, д. 17',
                                                   'latitude': 55.755826,
                                                   'longitude': 37.6173})

        self.assertEqual(get_user_model().objects.get(username='testuser').event_set.count(), 0)

    def test_event_create_success_view(self):
        response = self.client.get(reverse('event-create-success'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_event_successful.html')


class EventsFormTest(TestCase):
    def test_event_form(self):
        form = EventForm(data={'title': 'Test Event', 'datetime': '2023-08-01T12:00:00',
                               'description': 'Test Description', 'address': 'Москва, ул. Пушкина, д. 17',
                               'latitude': 55.755826, 'longitude': 37.6173})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test Event')
        self.assertEqual(form.cleaned_data['datetime'],
                         datetime(2023, 8, 1, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Moscow')))
        self.assertEqual(form.cleaned_data['description'], 'Test Description')
        self.assertEqual(form.cleaned_data['address'], 'Москва, ул. Пушкина, д. 17')
        self.assertEqual(form.cleaned_data['latitude'], 55.755826)
        self.assertEqual(form.cleaned_data['longitude'], 37.6173)

    def test_event_form_invalid_data(self):
        form = EventForm(data={'description': 'Test Description', 'latitude': 55.755826, 'longitude': 37.6173})
        self.assertFalse(form.is_valid())

    def test_event_form_empty_data(self):
        form = EventForm(data={})
        self.assertFalse(form.is_valid())
