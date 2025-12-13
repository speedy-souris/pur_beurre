from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup
from food_selection.models import Product, Category


class EmptyDBFoundTemplateTest(TestCase):
    """
    Tests whether the template returns only relevant substitutes.
    """
    def setUp(self):
        User = get_user_model()
        # user creation
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        # product creation
        self.product = Product.objects.create(
            product_id="1111111111111",
            name="Confiture de fraise",
            nutriscore="e"
        )

    def test_found_template_substitution_logic(self):
        response = self.client.get(reverse('food_selection:found'), {'product': 'confiture de fraise'})
        self.assertEqual(response.status_code, 200)

        # Verify that the specified template was used to render the page.
        self.assertTemplateUsed(response, 'food_selection/products.html')

class FoundTemplateWithSubstitutesTest(TestCase):
    """
       Check the number of substitutes displayed using BeautifulSoup.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Creates the initial data for testing
        """
        # 1. Creating categories
        category_confiture = Category.objects.create(name="Confitures")
        category_pate_a_tartiner = Category.objects.create(name="Pâtes à tartiner")

        # 2. Creation of the product that will be sought after (with a poor Nutri-Score)
        cls.product_to_find = Product.objects.create(
            product_id="3017620422003",
            name="Confiture de Fraise Classique",
            nutriscore="d"
        )
        cls.product_to_find.categories.add(category_confiture)

        # 3. Creation of 7 substitute products to test pagination, which is 6 products per page
        for i in range(7):
            product = Product.objects.create(
                product_id=f"0000{i}",
                name=f"Confiture Allégée {i+1}",
                nutriscore="a"
            )
            product.categories.add(category_confiture, category_pate_a_tartiner)

    def test_count_substitute_products_on_page(self):
        """
        Check that the page displays 6 substitute products (the limit per page)..
        """
        # Step 1: Simulate the user's GET request
        response = self.client.get(reverse('food_selection:found'), {'product': self.product_to_find.name})

        # Step 2: Checks on the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/products.html')

        # Step 3: response.content contains the raw HTML of the rendered page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Step 4: Count the items that correspond to a substitute product.
        substitute_products_divs = soup.select('div.substitute_products')
        # Step 5: Confirm that the number of items found is indeed 6.
        self.assertEqual(len(substitute_products_divs), 6)

    def test_count_substitute_products_on_page2(self):
        """
        Check that the page displays 6 substitute products (the limit per page)..
        """
        # Step 1: Simulate the user's GET request
        response = self.client.get(reverse('food_selection:found'), {'product': self.product_to_find.name,
                                                                     'page': 2})
        # Step 2: Checks on the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/products.html')

        # Step 3: response.content contains the raw HTML of the rendered page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Step 4: Count the items that correspond to a substitute product.
        substitute_products_divs = soup.select('div.substitute_products')
        # Step 5: Assert that the number of elements found is indeed 1
        self.assertEqual(len(substitute_products_divs), 1)