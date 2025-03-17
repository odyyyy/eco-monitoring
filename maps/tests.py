from unittest import mock

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse


class MapsViewTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @mock.patch('maps.views.get_average_aqi', mock.MagicMock(return_value=50))
    @mock.patch('maps.views.get_radiation_level', mock.MagicMock(return_value=0.1))
    @mock.patch('maps.views.get_air_temperature_and_weather_description', mock.MagicMock(return_value=(20, 'Солнечно')))
    @override_settings(CACHES={'pages_cache': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_maps_view_success_get_data_from_apis(self):
        response = self.client.get(reverse('maps'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'maps.html')
