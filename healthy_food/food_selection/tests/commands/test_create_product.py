import requests
from unittest.mock import patch, Mock
from django.core.management import call_command
from django.test import TestCase
from food_selection.models import Product, Category

# Simulated data that the OpenFoodFacts API could return
MOCK_API_RESPONSE = {
    "count": 4,
    "page": 1,
    "page_count": 100,
    "page_size": 100,
    "products": [
        # Case 1: Valid product WITH image
        {
            "code": "123456789",
            "product_name_fr": "Jus d'orange pur jus",
            "nutriscore_grade": "c",
            "url": "https://fr.openfoodfacts.org/produit/123456789",
            "image_url": "https://example.com/image.jpg",
            "categories_tags_fr": ["boissons", "jus-de-fruits"],
            "nutriments": {
                "sugars_100g": 8.9,
                "salt_100g": 0.01,
                "fat_100g": 0.5,
                "satured_fat_100g": 0.1,
                "une_cle_inutile": "valeur" # Doit être filtrée
            }
        },
        # Case 2: Valid product WITHOUT image (should receive default image)
         {
            "code": "987654321",
            "product_name_fr": "Eau Minérale",
            "nutriscore_grade": "a",
            "url": "https://fr.openfoodfacts.org/produit/987654321",
            "image_url": None, # URL invalide/manquante
            "categories_tags_fr": ["boissons"],
            "nutriments": {"salt_100g": 0.0}
        },
        # Case 3: Invalid product (incorrect Nutri-Score)
        {
            "code": "555555555",
            "product_name_fr": "Soda",
            "nutriscore_grade": "Z", # Nutriscore invalide
            "categories_tags_fr": ["boissons"],
            "nutriments": {}
        },
        # Case 4: Invalid product (should be ignored)
        {
            "code": "555555555",
            "product_name_fr": None, # Nom manquant
            "nutriscore_grade": "b",
            "categories_tags_fr": ["boissons"],
            "nutriments": {}
        }
    ]
}


class ImportProductsCommandTest(TestCase):

    # The decorator @patch intercepts ‘requests.get’ in the context of this test.
    # 'mock_get' is a mock object that replaces the original function.
    @patch('requests.get')
    def test_handle_command_success(self, mock_get):
        """
        Test the success of the import with simulated data.
        """
        # --- Mock Configuration ---
        # We configure the mock to behave like a successful API response.
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None  # Simulates an HTTP 200 OK response
        mock_response.json.return_value = MOCK_API_RESPONSE # Retourne nos données de test
        mock_get.return_value = mock_response

        # --- Execution ---
        # We call it management control.
        # The --silent option is useful for keeping the test output clean.
        call_command('create_product', '--silent')

        # --- Assertions ---
        # We verify that the database contains what we expect.

        # 1. Verify that the “beverages” category has been created.
        self.assertEqual(Category.objects.count(), 1)
        self.assertTrue(Category.objects.filter(name='boissons').exists())

        # 2. Verify that TWO products (both valid) have been created.
        self.assertEqual(Product.objects.count(), 2)

        # 3. Verify that only one product (the valid one) has been created.
        self.assertEqual(Product.objects.count(), 2)
        product = Product.objects.first()

        # 3. Verify that only one product (the valid one) has been created.
        self.assertEqual(product.name, "Jus d'orange pur jus")
        self.assertEqual(product.product_id, "123456789")
        self.assertEqual(product.nutriscore, "C") # Must be capitalized
        self.assertIn('sugars_100g', product.nutriments)
        self.assertNotIn('une_cle_inutile', product.nutriments) # Check that the filtering worked

        # 4. Check the Many-to-Many relationship.
        self.assertEqual(product.categories.count(), 1)
        self.assertEqual(product.categories.first().name, 'boissons')

        # 5. Verify that the API call has been made for each category.
        # The script has 10 categories to fetch.
        self.assertEqual(mock_get.call_count, 10)
        # You can even check the URL of the first call.
        first_call_url = mock_get.call_args_list[0][0][0] # Extract the URL from the first call
        self.assertIn("pâtes alimentaires  de céréales", first_call_url)

    @patch('requests.get')
    def test_handle_command_api_error(self, mock_get):
        """
        Tests the behavior of the command in case of an API error.
        """
        # --- Mock Configuration ---
        # We configure the mock to simulate a network error (e.g., 404, 500).
        mock_get.side_effect = requests.RequestException("Erreur de connexion simulée")

        # --- Exécution ---
        call_command('create_product', '--silent')

        # --- Assertions ---
        # We verify that no data has been added to the database.
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Product.objects.count(), 0)
