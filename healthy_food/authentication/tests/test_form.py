from django import forms
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.test import TestCase

from authentication.forms import LoginForm
from authentication.forms import SignupForm


class LoginFormTest(SimpleTestCase):

    def test_login_form_valid_data(self):
        """
        Test 1: Verify that the form is valid with correct data.
        """
        form_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['password'], 'password123')

    def test_login_form_empty_data(self):
        """
        Test 2: Verifies that the form generates errors if the fields are empty.
        """
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # We expect one error for username and one for password.
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_login_form_max_length(self):
        """
        Test 3: Checks the constraint max_length=63.
        """
        # We create a 64-character username (which is too long).
        long_username = 'a' * 64

        form_data = {
            'username': long_username,
            'password': 'password123'
        }
        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)  # Must contain an error in the username

    def test_login_form_labels(self):
        """
        Test 4: Verifies that the labels are correct (for HTML display).
        """
        form = LoginForm()
        self.assertEqual(form.fields['username'].label, 'Nom d’utilisateur')
        self.assertEqual(form.fields['password'].label, 'Mot de passe')

    def test_login_form_widget(self):
        """
        Test 5: Verify that the password field is hidden (PasswordInput widget).
        """
        form = LoginForm()
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)


class SignupFormTest(TestCase):

    def setUp(self):
        # We retrieve the active user model.
        self.User = get_user_model()

    def test_signup_form_valid(self):
        """
        Test 1: Nominal case. The data is correct, the user must be created.
        """
        form_data = {
            'username': 'nouveau_user',
            'email': 'test@example.com',
            'password1': 'MonMotDePasseSecret123!',  # Field required by UserCreationForm
            'password2': 'MonMotDePasseSecret123!',  # Confirmation required
        }
        form = SignupForm(data=form_data)

        self.assertTrue(form.is_valid())

        # We verify that the backup is working.
        user = form.save()
        self.assertEqual(user.username, 'nouveau_user')
        self.assertEqual(user.email, 'test@example.com')
        # We verify that the password is hashed (not in plain text).
        self.assertTrue(user.check_password('MonMotDePasseSecret123!'))

    def test_signup_form_password_mismatch(self):
        """
        Test 2: Passwords do not match.
        """
        form_data = {
            'username': 'user_fail',
            'email': 'fail@example.com',
            'password1': 'MotDePasseA',
            'password2': 'MotDePasseB',  # Different
        }
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        # The error is usually associated with the password2 field or non-field errors.
        self.assertIn('password2', form.errors)

    def test_signup_form_username_already_exists(self):
        """
        Test 3: The username is already taken (Uniqueness test).
        """
        # First, create a user in the database.
        self.User.objects.create_user(username='doublon', email='old@test.com', password='pwd')

        # We try to create the same
        form_data = {
            'username': 'doublon',  # Already taken
            'email': 'new@test.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ['Un utilisateur avec ce nom existe déjà.'])

    def test_signup_form_invalid_email(self):
        """
        Test 4: Email format validation.
        """
        form_data = {
            'username': 'user_email_fail',
            'email': 'ceci-n-est-pas-un-email',  # Invalid format
            'password1': 'password123',
            'password2': 'password123',
        }
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_signup_form_fields_list(self):
        """
        Test 5: Verify that only the username and email address are exposed (excluding passwords)...
        """
        form = SignupForm()
        # We check the ‘fields’ list defined in Meta.
        self.assertEqual(list(form.Meta.fields), ['username', 'email'])