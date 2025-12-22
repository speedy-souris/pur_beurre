from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class SignupTestCase(TestCase):
    User = get_user_model()
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('authentication:signup')

    def test_signup_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'nouvel_utilisateur',
            'email': 'nouvel_utilisateur@gmail.com',
            'password1': 'MotDePasseFort123!',
            'password2': 'MotDePasseFort123!',
        })
        self.assertEqual(self.User.objects.count(), 1)
        self.assertTrue(self.User.objects.filter(username='nouvel_utilisateur').exists())
        self.assertEqual(response.status_code, 302)  # redirection après succès

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'MotDePasse123!',
            'password2': 'AutreMotDePasse123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.User.objects.count(), 0)
        self.assertContains(response, 'password')

    def test_signup_existing_username(self):
        self.User.objects.create_user(
            username='pascal',
            password='MotDePasse123!'
        )
        response = self.client.post(self.signup_url, {
            'username': 'pascal',
            'email': 'pascal@test.com',
            'password1': 'MotDePasse123!',
            'password2': 'MotDePasse123!',
        })
        self.assertEqual(self.User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username')

    def test_signup_missing_fields(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.User.objects.count(), 0)
        self.assertTrue(response.context['form'].errors)
