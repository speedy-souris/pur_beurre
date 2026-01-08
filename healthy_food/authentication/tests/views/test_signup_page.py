from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse


class SignupPageViewTest(TestCase):

    def setUp(self):
        self.url = reverse('authentication:signup')
        self.User = get_user_model()

    def test_signup_page_display_get(self):
        """
        Test 1: Verify that the page displays correctly (GET).
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signup.html')

        # Checks for the presence of forms in the context
        self.assertIn('form', response.context)
        self.assertIn('search_form', response.context)

    def test_signup_success_post(self):
        """
        Test 2: Registration successful.
        """
        # Valid data for the form
        data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password1': 'SecretPassword123!',
            'password2': 'SecretPassword123!'
        }

        response = self.client.post(self.url, data)

        # 1. Verification of user creation in the database
        self.assertTrue(self.User.objects.filter(username='new_user').exists())

        # 2. Verify that the user is automatically logged in
        self.assertIn('_auth_user_id', self.client.session)

        # 3. Vérification de la redirection
        # The expected target URL is calculated via the settings.
        expected_url = resolve_url(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, expected_url)

        # 4. Success message verification
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Vous êtes Maintenant Inscrit !")

    def test_signup_failure_password_mismatch(self):
        """
        Test 3: Failure if passwords do not match.
        """
        data = {
            'username': 'fail_user',
            'email': 'fail@example.com',
            'password1': 'MotDePasseA',
            'password2': 'MotDePasseB'  # Different
        }

        response = self.client.post(self.url, data)

        # 1. No redirection, stay on the page (Code 200)
        self.assertEqual(response.status_code, 200)

        # 2. The user must NOT be created.
        self.assertFalse(self.User.objects.filter(username='fail_user').exists())

        # 3. The user must NOT be logged in.
        self.assertNotIn('_auth_user_id', self.client.session)

        # 4. The form must contain an error.
        form = response.context['form']
        self.assertFalse(form.is_valid())
        # The mismatch error is usually found in password2 or in non_field_errors.
        # Here we simply check for errors.
        self.assertTrue(len(form.errors) > 0)