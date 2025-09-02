from django.core.management import call_command
from django.test import TestCase
from food_selection.models import Product, Category


class DeleteAllDataCommandTest(TestCase):

    def test_handle_deletes_all_data(self):
        """
        Test that the command deletes all products and categories.
        """
        # --- 1. SETUP ---
        # Create a few objects in the test database.
        Category.objects.create(name="Catégorie Test 1")
        Category.objects.create(name="Catégorie Test 2")

        Product.objects.create(
            name="Produit Test 1",
            product_id="1111",
            nutriscore="A",
            nutriments={"salt": 0.1}
        )
        Product.objects.create(
            name="Produit Test 2",
            product_id="2222",
            nutriscore="B",
            nutriments={"sugar": 5}
        )

        # --- 2. PRE-ASSERTION (best practice) ---
        # Verify that the data exists BEFORE executing the command.
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Category.objects.count(), 2)

        # --- 3. EXECUTION ---
        # Call your management order.
        # Ensure that the name of your command file is ‘delete_all_data.py’.
        call_command('delete_all_data', '--silent')

        # --- 4. POST-ASSERTION ---
        # Verify that the database is now empty.
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)