from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse


class SignupPageViewTest(TestCase):

    def setUp(self):
        self.url = reverse('authentication:signup')  # Assurez-vous que le nom est bon
        self.User = get_user_model()

    def test_signup_page_display_get(self):
        """
        Test 1: Vérifie que la page s'affiche correctement (GET).
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/signup.html')

        # Vérifie la présence des formulaires dans le contexte
        self.assertIn('form', response.context)
        self.assertIn('search_form', response.context)

    def test_signup_success_post(self):
        """
        Test 2: Inscription réussie.
        """
        # Données valides pour le formulaire
        data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password1': 'SecretPassword123!',
            'password2': 'SecretPassword123!'
        }

        response = self.client.post(self.url, data)

        # 1. Vérification de la création de l'utilisateur en BDD
        self.assertTrue(self.User.objects.filter(username='new_user').exists())

        # 2. Vérification que l'utilisateur est connecté automatiquement
        self.assertIn('_auth_user_id', self.client.session)

        # 3. Vérification de la redirection
        # On calcule l'URL cible attendue via les settings
        expected_url = resolve_url(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, expected_url)

        # 4. Vérification du message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Vous êtes Maintenant Inscrit !")

    def test_signup_failure_password_mismatch(self):
        """
        Test 3: Échec si les mots de passe ne correspondent pas.
        """
        data = {
            'username': 'fail_user',
            'email': 'fail@example.com',
            'password1': 'MotDePasseA',
            'password2': 'MotDePasseB'  # Différent
        }

        response = self.client.post(self.url, data)

        # 1. Pas de redirection, on reste sur la page (Code 200)
        self.assertEqual(response.status_code, 200)

        # 2. L'utilisateur ne doit PAS être créé
        self.assertFalse(self.User.objects.filter(username='fail_user').exists())

        # 3. L'utilisateur ne doit PAS être connecté
        self.assertNotIn('_auth_user_id', self.client.session)

        # 4. Le formulaire doit contenir une erreur
        form = response.context['form']
        self.assertFalse(form.is_valid())
        # L'erreur de correspondance se trouve généralement sur password2 ou dans non_field_errors
        # Ici on vérifie simplement qu'il y a des erreurs
        self.assertTrue(len(form.errors) > 0)