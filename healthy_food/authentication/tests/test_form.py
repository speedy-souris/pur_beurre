from django import forms
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.test import TestCase

from authentication.forms import LoginForm
from authentication.forms import SignupForm


class LoginFormTest(SimpleTestCase):

    def test_login_form_valid_data(self):
        """
        Test 1: Vérifie que le formulaire est valide avec des données correctes.
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
        Test 2: Vérifie que le formulaire génère des erreurs si les champs sont vides.
        """
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # On attend une erreur pour username et une pour password
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_login_form_max_length(self):
        """
        Test 3: Vérifie la contrainte max_length=63.
        """
        # On crée un pseudo de 64 caractères (donc trop long)
        long_username = 'a' * 64

        form_data = {
            'username': long_username,
            'password': 'password123'
        }
        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)  # Doit contenir une erreur sur le username

    def test_login_form_labels(self):
        """
        Test 4: Vérifie que les étiquettes (labels) sont correctes (pour l'affichage HTML).
        """
        form = LoginForm()
        self.assertEqual(form.fields['username'].label, 'Nom d’utilisateur')
        self.assertEqual(form.fields['password'].label, 'Mot de passe')

    def test_login_form_widget(self):
        """
        Test 5: Vérifie que le champ password est bien caché (widget PasswordInput).
        """
        form = LoginForm()
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)


class SignupFormTest(TestCase):

    def setUp(self):
        # On récupère le modèle utilisateur actif
        self.User = get_user_model()

    def test_signup_form_valid(self):
        """
        Test 1: Cas nominal. Les données sont correctes, l'utilisateur doit être créé.
        """
        form_data = {
            'username': 'nouveau_user',
            'email': 'test@example.com',
            'password1': 'MonMotDePasseSecret123!',  # Champ requis par UserCreationForm
            'password2': 'MonMotDePasseSecret123!',  # Confirmation requise
        }
        form = SignupForm(data=form_data)

        self.assertTrue(form.is_valid())

        # On vérifie que la sauvegarde fonctionne
        user = form.save()
        self.assertEqual(user.username, 'nouveau_user')
        self.assertEqual(user.email, 'test@example.com')
        # On vérifie que le mot de passe est bien haché (pas en clair)
        self.assertTrue(user.check_password('MonMotDePasseSecret123!'))

    def test_signup_form_password_mismatch(self):
        """
        Test 2: Les mots de passe ne correspondent pas.
        """
        form_data = {
            'username': 'user_fail',
            'email': 'fail@example.com',
            'password1': 'MotDePasseA',
            'password2': 'MotDePasseB',  # Différent
        }
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        # L'erreur est généralement associée au champ password2 ou non-field errors
        self.assertIn('password2', form.errors)

    def test_signup_form_username_already_exists(self):
        """
        Test 3: Le nom d'utilisateur est déjà pris (Test d'unicité).
        """
        # On crée d'abord un utilisateur en base
        self.User.objects.create_user(username='doublon', email='old@test.com', password='pwd')

        # On essaie de créer le même
        form_data = {
            'username': 'doublon',  # Déjà pris
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
        Test 4: Validation du format de l'email.
        """
        form_data = {
            'username': 'user_email_fail',
            'email': 'ceci-n-est-pas-un-email',  # Format invalide
            'password1': 'password123',
            'password2': 'password123',
        }
        form = SignupForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_signup_form_fields_list(self):
        """
        Test 5: Vérifie que seuls username et email sont exposés (hors mots de passe).
        """
        form = SignupForm()
        # On vérifie la liste 'fields' définie dans Meta
        self.assertEqual(list(form.Meta.fields), ['username', 'email'])