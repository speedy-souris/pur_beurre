from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

from authentication.forms import LoginForm


class LoginTestCase(TestCase):
    User = get_user_model()
    def setUp(self):
        self.client = Client()
        self.user = self.User.objects.create_user(
            username='pascal',
            password='motdepasse123'
        )
        self.login_url = reverse('authentication:login')
        self.protected_url = reverse('food_selection:save_products')

    # ---------- Login successful ----------
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        # Redirection after login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # ---------- Incorrect password ----------
    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'fauxmotdepasse'
        })
        # Form reloaded with error
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- User does not exist ----------
    def test_login_unknown_user(self):
        response = self.client.post(self.login_url, {
            'username': 'ghost',
            'password': 'whatever'
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Inactive user ----------
    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Access to protected page ----------
    def test_authenticated_user_can_access_protected_page(self):
        # Login via the POST form to simulate the real flow
        self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)

    # ---------- Redirection for anonymous users ----------
    def test_anonymous_user_redirected(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    # ---------- Redirection with next ----------
    def test_login_redirect_next(self):
        next_url = self.protected_url
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123',
            'next': next_url
        })
        self.assertRedirects(response, next_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # ---------- Checking error messages ----------
    def test_login_error_message(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'mauvaismdp'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Verify that hidden next is present ----------
    def test_login_form_contains_next(self):
        next_url = self.protected_url
        response = self.client.get(self.login_url + f'?next={next_url}')
        self.assertContains(response, f'name="next" value="{next_url}"')
