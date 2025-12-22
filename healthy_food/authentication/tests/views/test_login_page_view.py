from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class LoginPageViewTest(TestCase):

    def setUp(self):
        # Création d'un utilisateur pour tester la connexion réussie
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('authentication:login')

    def test_login_page_display(self):
        """
        Test GET: Vérifie que la page s'affiche avec les bons contextes.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

        # Vérifie la présence des formulaires dans le contexte
        self.assertIn('form', response.context)  # LoginForm
        self.assertIn('search_form', response.context)  # SearchNewFood

    def test_login_success_redirects_home(self):
        """
        Test POST: Connexion réussie -> Redirection vers l'accueil.
        """
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.url, data)

        # Vérifie la redirection vers 'food_selection:home'
        self.assertRedirects(response, reverse('food_selection:home'))

        # Vérifie que l'utilisateur est bien connecté (session active)
        self.assertIn('_auth_user_id', self.client.session)

        # Vérifie le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Vous avez été connecté avec succès !")

    def test_login_success_redirects_next(self):
        """
        Test POST: Connexion réussie avec paramètre 'next' -> Redirection vers 'next'.
        """
        # On simule un champ caché 'next' dans le formulaire
        data = {
            'username': 'testuser',
            'password': 'password123',
            'next': '/some/protected/url/'
        }
        response = self.client.post(self.url, data)

        # Note: assertRedirects vérifie le code 302 et l'URL cible
        self.assertRedirects(response, '/some/protected/url/', fetch_redirect_response=False)

    def test_login_failed_invalid_credentials(self):
        """
        Test POST: Mauvais mot de passe -> Reste sur la page + Message erreur.
        """
        data = {
            'username': 'testuser',
            'password': 'MAUVAIS_PASSWORD'
        }
        response = self.client.post(self.url, data)

        # Code 200 attendu (pas de redirection, on réaffiche la page avec l'erreur)
        self.assertEqual(response.status_code, 200)

        # Vérifie que l'utilisateur n'est PAS connecté
        self.assertNotIn('_auth_user_id', self.client.session)

        # Vérifie le message d'erreur spécifique défini dans votre vue
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Identifiant ou mot de passe invalide.')

    def test_login_failed_invalid_form(self):
        """
        Test POST: Champs vides -> Message erreur spécifique 'Veuillez vérifier...'.
        """
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        # Vérifie le message d'erreur pour formulaire invalide
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Veuillez vérifier les champs du formulaire.')