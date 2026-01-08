from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


class LogoutViewTest(TestCase):

    def setUp(self):
        # 1. We create a user and log them in.
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

    def test_logout_user(self):
        """
        Verify that the view logs the user out, redirects, and displays a message.
        """
        url = reverse('authentication:logout')

        # Action: Call the logout URL
        response = self.client.get(url)

        self.assertRedirects(response, reverse('food_selection:home'))

        # '_auth_user_id' is the session key for storing the logged-in user ID.
        self.assertNotIn('_auth_user_id', self.client.session)

        # 3. Success message verification
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Vous êtes déconnecté !")