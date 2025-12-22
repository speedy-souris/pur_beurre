from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class SignupAutoLoginTestCase(TestCase):
    User = get_user_model()
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('authentication:signup')

    def test_user_is_logged_in_after_signup(self):
        response = self.client.post(self.signup_url, {
            'username': 'nouveau',
            'email': 'nouveau@test.com',
            'password1': 'MotDePasseFort123!',
            'password2': 'MotDePasseFort123!',
        }, follow=True)
        user = self.User.objects.get(username='nouveau')
        self.assertTrue(user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
