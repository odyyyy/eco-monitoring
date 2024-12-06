from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from problems.forms import EcoProblemReportForm


class ProblemViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        self.client.force_login(self.user)

    def test_report_create_view_get(self):
        response = self.client.get(reverse('report_problem'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_problem.html')

    def test_report_create_view_post(self):
        response = self.client.post(reverse('report_problem'), {'title': 'Test Problem',
                                                                'description': 'Test Description',
                                                                'address': 'Москва, ул. Пушкина, д. 17',
                                                                'latitude': 55.755826,
                                                                'longitude': 37.6173})

        self.assertRedirects(response, reverse('report_problem_success'))
        self.assertEqual(get_user_model().objects.get(username='testuser').ecoproblem_set.count(), 1)

    def test_report_create_view_invalid_data(self):
        self.client.post(reverse('report_problem'), {
            'description': 'Test Description',
            'latitude': 55.755826,
            'longitude': 37.6173})

        self.assertEqual(get_user_model().objects.get(username='testuser').ecoproblem_set.count(), 0)

    def test_report_create_success_view(self):
        response = self.client.get(reverse('report_problem_success'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_problem_successful.html')


class ProblemFormsTest(TestCase):
    def test_eco_problem_report_form(self):
        form = EcoProblemReportForm(data={'title': 'Test Problem', 'description': 'Test Description',
                                          'address': 'Москва, ул. Пушкина, д. 17',
                                          'latitude': 55.755826, 'longitude': 37.6173})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test Problem')
        self.assertEqual(form.cleaned_data['description'], 'Test Description')
        self.assertEqual(form.cleaned_data['address'], 'Москва, ул. Пушкина, д. 17')
        self.assertEqual(form.cleaned_data['latitude'], 55.755826)
        self.assertEqual(form.cleaned_data['longitude'], 37.6173)

    def test_eco_problem_report_form_empty_data(self):
        form = EcoProblemReportForm(data={})
        self.assertFalse(form.is_valid())

    def test_eco_problem_report_form_invalid_data(self):
        form = EcoProblemReportForm(data={'description': 'Test Description', 'latitude': 55.755826, 'longitude': 37.6173})
        self.assertFalse(form.is_valid())
