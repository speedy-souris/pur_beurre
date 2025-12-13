from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from food_selection.models import Product, Favorite

class SaveProductFormViewTest(TestCase):
    def setUp(self):
        # 1. User Creation and Login (Required for LoginRequiredMixin)
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_login(self.user)

        #2. Product creation
        self.product = Product.objects.create(
            name="Pâtes complètes",
            product_id="123456",
            nutriscore="A",
            nutriments={"sugars_100g": 5, "salt_100g": 0.01},
            url="http://example.com",
            image_url="http://example.com/image.jpg",
        )

    def test_save_product_success(self):
       # verification of the saved product
        url = reverse("food_selection:save_products")
        response = self.client.post(url, {"product_id": self.product.product_id})

       #1. Verifying redirection to the favorites list
        self.assertRedirects(response, reverse('food_selection:saved-list'))
       #2. LOGICAL check: A Favorite object must have been created.
        is_favorite = Favorite.objects.filter(user=self.user, product=self.product).exists()
        self.assertTrue(is_favorite)

    def test_save_product_does_not_exist(self):
        # Invalid ID during backup
        url = reverse("food_selection:save_products")
        response = self.client.post(url, {"product_id": '9999'})  # non-existent

        # 1. The view uses get_object_or_404, so we expect a 404 (Not Found) code
        # and not a redirection.
        self.assertEqual(response.status_code, 404)
        #2. Check that no favorites have been created by mistake.
        self.assertEqual(Favorite.objects.count(), 0)

    def test_redirect_if_not_logged_in(self):
        """
        Bonus test: Verify that LoginRequiredMixin does its job
        """
        self.client.logout()  # The user is disconnected.
        url = reverse("food_selection:save_products")
        response = self.client.post(url, {"product_id": self.product.product_id})

        # Must redirect to the login page (code 302)
        self.assertEqual(response.status_code, 302)
        # No favorites should be created
        self.assertEqual(Favorite.objects.count(), 0)