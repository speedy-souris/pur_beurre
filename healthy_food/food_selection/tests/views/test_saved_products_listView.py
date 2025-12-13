from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from food_selection.models import Product, Favorite

class SavedProductsListViewTest(TestCase):
    def setUp(self):
        # 1. USER CREATION (Essential for viewing)
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)
        # Saved product
        self.saved_product = Product.objects.create(
            name="Riz complet",
            product_id="111111",
            nutriscore="A",
            nutriments={"sugars_100g": 1, "salt_100g": 0.01},
            url="http://example.com/riz",
            image_url="http://example.com/riz.jpg",
        )
        # Create the “Favorite” link for the logged-in user
        Favorite.objects.create(user=self.user, product=self.saved_product)

        # Product NOT saved
        self.unsaved_product = Product.objects.create(
            name="Chips",
            product_id="222222",
            nutriscore="E",
            nutriments={"sugars_100g": 15, "salt_100g": 2},
            url="http://example.com/chips",
            image_url="http://example.com/chips.jpg",
        )

    def test_only_saved_products_listed(self):
        # Verify that only products with saved=True appear
        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz complet")   # must appear
        self.assertNotContains(response, "Chips")      # should NOT appear

    def test_context_contains_expected_keys(self):
           # Verify that the context contains search_form, page_obj, and page_name.
        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        self.assertIn("search_form", response.context)
        self.assertIn("page_obj", response.context)
        self.assertEqual(response.context["page_name"], "Mes Favoris")

    def test_pagination_limit(self):
        # Verify that pagination is limited to 6 products per page
        # We create 12 saved products.
        for i in range(12):
            prod = Product.objects.create(
                name=f"Produit {i}",
                product_id=f"p{i}",
                nutriscore="B",
                nutriments={},
                url=f"http://example.com/{i}",
                image_url=f"http://example.com/{i}.jpg",
            )
            # IMPORTANT: Create the favorite so that it is counted by the view.
            Favorite.objects.create(user=self.user, product=prod)

        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 6)  # must be limited to 6
        self.assertTrue(page_obj.has_next())  # must have a second page

    def test_redirect_if_not_logged_in(self):
        """
        Verify that a user who is not logged in is redirected.
        """
        self.client.logout()
        url = reverse("food_selection:saved-list")
        response = self.client.get(url)
        # Redirect to login (302)
        self.assertEqual(response.status_code, 302)