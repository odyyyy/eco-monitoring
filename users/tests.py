from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.forms import UserSignUpForm


class UsersViewTests(TestCase):

    def test_sign_up_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_sign_up_view_register_user(self):
        response = self.client.post(reverse('signup'),
                                    {'username': 'testuser', 'password': 'testpassword', 'password2': 'testpassword'})
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(get_user_model().objects.get(username='testuser').username, 'testuser')

    def test_profile_view_get_user_authenticated(self):
        self.client.force_login(get_user_model().objects.create_user(username='testuser', password='testpassword123'))
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_get_user_not_authenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('profile'))


class UsersFormsTests(TestCase):

    def test_user_sign_up_form(self):
        form = UserSignUpForm(data={'username': 'testuser', 'password': 'testpassword', 'password2': 'testpassword'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['password'], 'testpassword')
        self.assertEqual(form.cleaned_data['password2'], 'testpassword')

    def test_user_sign_up_form_not_same_password(self):
        form = UserSignUpForm(data={'username': 'testuser', 'password': 'testpassword', 'password2': 'testpassword123'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['Пароли не совпадают.'])

