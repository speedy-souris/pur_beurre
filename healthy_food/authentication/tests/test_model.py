from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase


class UserModelTest(TestCase):

    def setUp(self):
        # We always retrieve the model via get_user_model()
        # to ensure that the one defined in settings.AUTH_USER_MODEL is used
        self.User = get_user_model()

    def test_create_user_with_valid_data(self):
        """
        Test 1: Verify that a standard user can be created.
        """
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)  # Default True in AbstractUser

    def test_email_is_unique(self):
        """
        Test 2: Verify that the single constraint=True on the email is working.
        This is the most important test because AbstractUser does not impose it by default.
        """
        # Creating the first user
        self.User.objects.create_user(
            username='user1',
            email='unique@example.com',
            password='pwd'
        )

        # Attempt to create a second user with the SAME email address
        # This should raise an IntegrityError in the database.
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username='user2',
                email='unique@example.com',  # Duplicate
                password='pwd'
            )

    def test_role_default_value(self):
        """
        Test 3: Verify that the default role is ‘SUBSCRIBER’.
        """
        user = self.User.objects.create_user(
            username='roleuser',
            email='role@example.com',
            password='pwd'
        )

        self.assertEqual(user.role, 'SUBSCRIBER')

    def test_str_method(self):
        """
        Test 4: Check the __str__ method.
        """
        user = self.User.objects.create_user(username='my_name', email='s@t.com')
        self.assertEqual(str(user), 'my_name')

    def test_required_fields_configuration(self):
        """
        Test 5: Verify the configuration of the required fields (useful for createsuperuser).
        """
        # USERNAME_FIELD must be 'username'
        self.assertEqual(self.User.USERNAME_FIELD, 'username')
        # REQUIRED_FIELDS must contain 'email'
        self.assertIn('email', self.User.REQUIRED_FIELDS)