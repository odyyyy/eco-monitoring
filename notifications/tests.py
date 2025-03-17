from django.test import TestCase
from unittest import mock

from django.contrib.auth import get_user_model
from notifications.models import NotificationOption

from notifications.forms import NotificationOptionsForm
from notifications.tasks import send_notification_if_danger_level


class NotificationsFormsTest(TestCase):

    def test_notification_form(self):
        form = NotificationOptionsForm(data={'notification_options': ['1', '2']})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['notification_options'], ['1', '2'])

        form = NotificationOptionsForm(data={'notification_options': []})
        self.assertFalse(form.is_valid())

        form = NotificationOptionsForm(data={'notification_options': ['3']})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['notification_options'], ['3'])


class NotificationsTasksTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        NotificationOption.objects.create(user=self.user, notification_type=1)
        NotificationOption.objects.create(user=self.user, notification_type=2)

    @mock.patch('notifications.tasks.get_average_aqi', mock.MagicMock(return_value=50))
    @mock.patch('notifications.tasks.get_radiation_level', mock.MagicMock(return_value=0.1))
    @mock.patch('notifications.tasks.get_weather_id_and_status_from_forecast', mock.MagicMock(return_value=(801, 'Солнечно')))
    @mock.patch('notifications.tasks.send_mail')
    def test_send_notification_if_not_danger_level(self, mock_send_mail):
        is_send = send_notification_if_danger_level()

        mock_send_mail.assert_not_called()
        self.assertFalse(is_send)

    @mock.patch('notifications.tasks.get_average_aqi', mock.MagicMock(return_value=50))
    @mock.patch('notifications.tasks.get_radiation_level', mock.MagicMock(return_value=0.1))
    @mock.patch('notifications.tasks.get_weather_id_and_status_from_forecast', mock.MagicMock(return_value=(503, 'Ураган')))
    @mock.patch('notifications.tasks.send_mail')
    def test_send_notification_if_danger_level(self, mock_send_mail):
        is_send = send_notification_if_danger_level()

        mock_send_mail.assert_called_once()
        self.assertTrue(is_send)

    @mock.patch('notifications.tasks.get_average_aqi', mock.MagicMock(return_value=50))
    @mock.patch('notifications.tasks.get_radiation_level', mock.MagicMock(return_value=321))
    @mock.patch('notifications.tasks.get_weather_id_and_status_from_forecast', mock.MagicMock(return_value=(801, 'Солнечно')))
    @mock.patch('notifications.tasks.send_mail')
    def test_not_send_notification_if_danger_rad_user_not_subscribed_to_rad(self, mock_send_mail):
        is_send = send_notification_if_danger_level()

        mock_send_mail.assert_not_called()
        self.assertFalse(is_send)


    @mock.patch('notifications.tasks.get_average_aqi', mock.MagicMock(return_value=1230))
    @mock.patch('notifications.tasks.get_radiation_level', mock.MagicMock(return_value=321))
    @mock.patch('notifications.tasks.get_weather_id_and_status_from_forecast', mock.MagicMock(return_value=(801, 'Солнечно')))
    @mock.patch('notifications.tasks.send_mail')
    def test_send_notification_if_danger_radiation_air_user_not_subscribed_to_radiation(self, mock_send_mail):
        is_send = send_notification_if_danger_level()

        mock_send_mail.assert_called_once()
        self.assertTrue(is_send)