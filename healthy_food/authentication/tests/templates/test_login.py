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

    # ---------- Login réussi ----------
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        # Redirection après login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # ---------- Mauvais mot de passe ----------
    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'fauxmotdepasse'
        })
        # Formulaire rechargé avec erreur
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Utilisateur inexistant ----------
    def test_login_unknown_user(self):
        response = self.client.post(self.login_url, {
            'username': 'ghost',
            'password': 'whatever'
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Utilisateur inactif ----------
    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Accès à page protégée ----------
    def test_authenticated_user_can_access_protected_page(self):
        # Login via le formulaire POST pour simuler le vrai flux
        self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123'
        })
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)

    # ---------- Redirection pour utilisateur anonyme ----------
    def test_anonymous_user_redirected(self):
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    # ---------- Redirection avec next ----------
    def test_login_redirect_next(self):
        next_url = self.protected_url
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'motdepasse123',
            'next': next_url
        })
        self.assertRedirects(response, next_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # ---------- Vérification des messages d'erreur ----------
    def test_login_error_message(self):
        response = self.client.post(self.login_url, {
            'username': 'pascal',
            'password': 'mauvaismdp'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # ---------- Vérification que le hidden next est présent ----------
    def test_login_form_contains_next(self):
        next_url = self.protected_url
        response = self.client.get(self.login_url + f'?next={next_url}')
        self.assertContains(response, f'name="next" value="{next_url}"')
