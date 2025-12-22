from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class UserModelTest(TestCase):

    def setUp(self):
        # On récupère toujours le modèle via get_user_model()
        # pour être sûr d'utiliser celui défini dans settings.AUTH_USER_MODEL
        self.User = get_user_model()

    def test_create_user_with_valid_data(self):
        """
        Test 1: Vérifie qu'on peut créer un utilisateur standard.
        """
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)  # Par défaut True dans AbstractUser

    def test_email_is_unique(self):
        """
        Test 2: Vérifie que la contrainte unique=True sur l'email fonctionne.
        C'est le test le plus important car AbstractUser ne l'impose pas par défaut.
        """
        # Création du premier utilisateur
        self.User.objects.create_user(
            username='user1',
            email='unique@example.com',
            password='pwd'
        )

        # Tentative de création d'un second utilisateur avec le MEME email
        # Cela doit lever une erreur d'intégrité (IntegrityError) au niveau de la DB
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username='user2',
                email='unique@example.com',  # Doublon
                password='pwd'
            )

    def test_role_default_value(self):
        """
        Test 3: Vérifie que le rôle par défaut est bien 'SUBSCRIBER'.
        """
        user = self.User.objects.create_user(
            username='roleuser',
            email='role@example.com',
            password='pwd'
        )

        self.assertEqual(user.role, 'SUBSCRIBER')

    def test_str_method(self):
        """
        Test 4: Vérifie la méthode __str__.
        """
        user = self.User.objects.create_user(username='my_name', email='s@t.com')
        self.assertEqual(str(user), 'my_name')

    def test_required_fields_configuration(self):
        """
        Test 5: Vérifie la configuration des champs requis (utile pour createsuperuser).
        """
        # USERNAME_FIELD doit être 'username'
        self.assertEqual(self.User.USERNAME_FIELD, 'username')
        # REQUIRED_FIELDS doit contenir 'email'
        self.assertIn('email', self.User.REQUIRED_FIELDS)