from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup
from food_selection.models import Product, Category, Favorite


class SavedTemplateWithFavoritesTest(TestCase):
    """
       Check the number of products saved to favorites.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Creates initial data for registered product tests
        """
        User = get_user_model()
        # user creation
        cls.user = User.objects.create_user(username='testuser', password='password')

        # 1. Creating categories
        category_confiture = Category.objects.create(name="Confitures")
        category_pate_a_tartiner = Category.objects.create(name="Pâtes à tartiner")
        # 2. Creation of 7 favorite products to test pagination, which is 6 products per page
        for i in range(7):
            favorites_product = Product.objects.create(
                product_id=f"0000{i}",
                name=f"Confiture Allégée {i + 1}",
                nutriscore="a"
            )
            favorites_product.categories.add(category_confiture, category_pate_a_tartiner)

            Favorite.objects.create(user=cls.user, product=favorites_product)

    def setUp(self):
        self.client.force_login(self.user)

    def test_count_favorites_products_on_page(self):
        """
        Check that the page displays 6 products in favorites (the limit per page)..
        """
        # Étape 1: Simulate the user's GET request
        response = self.client.get(reverse('food_selection:saved-list'))

        # Étape 2: Checks on the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/saved_products.html')

        # Étape 3: response.content contains the raw HTML of the rendered page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Count the items that match a favorite product
        favorites_products_divs = soup.select('div.favorite_saved_products')
        # Étape 5: Confirm that the number of items found is indeed 6.
        self.assertEqual(len(favorites_products_divs), 6)

    def test_count_favorite_products_on_page2(self):
        """
        Vérifie que la page affiche bien 1 produits en favoris.
        """
        # Step 1: Simulate the user's GET request
        response = self.client.get(reverse('food_selection:saved-list'), {'page': 2})
        # Étape 2: Checks on the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/saved_products.html')

        # Étape 3: response.content contains the raw HTML of the rendered page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Count the items that match a product in favorites
        favorite_products_divs = soup.select('div.favorite_saved_products')
        # Étape 5: Assert that the number of elements found is indeed 1
        self.assertEqual(len(favorite_products_divs), 1)