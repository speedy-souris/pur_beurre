from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


class LogoutViewTest(TestCase):

    def setUp(self):
        # 1. On crée un utilisateur et on le connecte
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

    def test_logout_user(self):
        """
        Vérifie que la vue déconnecte l'utilisateur, redirige et affiche un message.
        """
        url = reverse('authentication:logout')

        # Action : Appel de l'URL de déconnexion
        response = self.client.get(url)

        self.assertRedirects(response, reverse('food_selection:home'))

        # '_auth_user_id' est la clé de session pour stocker l'ID utilisateur connecté
        self.assertNotIn('_auth_user_id', self.client.session)

        # 3. Vérification du message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Vous êtes déconnecté !")