from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class LoginPageViewTest(TestCase):

    def setUp(self):
        # Creating a user to test the successful connection
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('authentication:login')

    def test_login_page_display(self):
        """
        GET test: Verifies that the page displays with the correct contexts.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

        # Checks for the presence of forms in the context
        self.assertIn('form', response.context)  # LoginForm
        self.assertIn('search_form', response.context)  # SearchNewFood

    def test_login_success_redirects_home(self):
        """
        POST test: Successful login -> Redirect to home page.
        """
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.url, data)

        # Check the redirect to 'food_selection:home'
        self.assertRedirects(response, reverse('food_selection:home'))

        # Verify that the user is logged in (active session)
        self.assertIn('_auth_user_id', self.client.session)

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Vous avez été connecté avec succès !")

    def test_login_success_redirects_next(self):
        """
        POST test: Successful connection with ‘next’ parameter -> Redirection to 'next'.
        """
        # We simulate a hidden ‘next’ field in the form.
        data = {
            'username': 'testuser',
            'password': 'password123',
            'next': '/some/protected/url/'
        }
        response = self.client.post(self.url, data)

        # Note: assertRedirects checks for code 302 and the target URL.
        self.assertRedirects(response, '/some/protected/url/', fetch_redirect_response=False)

    def test_login_failed_invalid_credentials(self):
        """
        POST test: Incorrect password -> Remains on the page + Error message.
        """
        data = {
            'username': 'testuser',
            'password': 'MAUVAIS_PASSWORD'
        }
        response = self.client.post(self.url, data)

        # Expected code 200 (no redirection, the page with the error is displayed again)
        self.assertEqual(response.status_code, 200)

        # Verify that the user is NOT logged in
        self.assertNotIn('_auth_user_id', self.client.session)

        # Check the specific error message defined in your view.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Identifiant ou mot de passe invalide.')

    def test_login_failed_invalid_form(self):
        """
        POST test: Empty fields -> Specific error message 'Please check...'.
        """
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        # Check the error message for invalid form
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Veuillez vérifier les champs du formulaire.')