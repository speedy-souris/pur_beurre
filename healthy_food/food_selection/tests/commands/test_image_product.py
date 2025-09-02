import os
import tempfile
import requests
from unittest.mock import patch, Mock

from django.core.management import call_command
from django.test import TestCase, override_settings
from food_selection.models import Product

# Create a temporary directory that will be used as the root for our tests.
# It's cleaner and more reliable than mocking ‘open’ or ‘os.makedirs’.
TEMP_MEDIA_ROOT = tempfile.TemporaryDirectory()


# We use override_settings to tell Django to use our temporary folder.
# as BASE_DIR for the duration of this test class.
# The directory will be automatically cleaned up at the end.
@override_settings(BASE_DIR=TEMP_MEDIA_ROOT.name)
class ImageProductCommandTest(TestCase):

    def tearDown(self):
        # Ensures that the directory contents are clean between each test
        for root, dirs, files in os.walk(TEMP_MEDIA_ROOT.name, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    @patch('requests.get')
    def test_handle_downloads_images_successfully(self, mock_get):
        """
        Tests the case where images are downloaded successfully.
        """
        # --- 1. SETUP ---
        # Configure the mock to simulate a successful HTTP response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'contenu-image-fictif' # Simulate the binary content of an image
        mock_get.return_value = mock_response

        # Create products in the test database
        Product.objects.create(
            product_id="123",
            name="Produit avec image",
            image_url="http://example.com/image1.jpg",
            nutriscore="A"
        )
        Product.objects.create(
            product_id="456",
            name="Produit sans image URL",
            image_url="", # This product should be ignored.
            nutriscore="B"
        )

        # --- 2. EXECUTION ---
        # Call the command to be tested
        call_command('image_product', '--silent')

        # --- 3. ASSERTIONS ---
        # Verify that requests.get was called only once (for the valid product)
        mock_get.assert_called_once_with("http://example.com/image1.jpg", timeout=10)

        # Build the path to the expected file in our temporary directory
        expected_dir = os.path.join(TEMP_MEDIA_ROOT.name, 'food_selection', 'static', 'food_selection', 'images', 'image_product')
        expected_file_path = os.path.join(expected_dir, "123.jpg")

        # Verify that the directory and file have been created
        self.assertTrue(os.path.exists(expected_dir))
        self.assertTrue(os.path.exists(expected_file_path))

        # Verify that the file contents are correct.
        with open(expected_file_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'contenu-image-fictif')

    @patch('requests.get')
    def test_handle_request_exception(self, mock_get):
        """
        Tests the case where the download fails due to a network error.
        """
        # --- 1. SETUP ---
        # Configure the mock to throw an exception
        mock_get.side_effect = requests.RequestException("Erreur de connexion simulée")

        Product.objects.create(
            product_id="789",
            name="Produit avec URL invalide",
            image_url="http://example.com/image_invalide.jpg",
            nutriscore="C"
        )

        # --- 2. EXECUTION ---
        call_command('image_product', '--silent')

        # --- 3. ASSERTIONS ---
        # Verify that requests.get has been called
        mock_get.assert_called_once_with("http://example.com/image_invalide.jpg", timeout=10)

        # Build the path to the file that should NOT exist
        expected_file_path = os.path.join(
            TEMP_MEDIA_ROOT.name, 'food_selection', 'static', 'food_selection', 'images', 'image_product', "789.jpg"
        )

        # Verify that the file has NOT been created
        self.assertFalse(os.path.exists(expected_file_path))