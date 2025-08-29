from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product

class SaveProductFormViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Pâtes complètes",
            product_id="123456",
            nutriscore="A",
            nutriments={"sugars_100g": 5, "salt_100g": 0.01},
            url="http://example.com",
            image_url="http://example.com/image.jpg",
            saved=False,  # By default
        )

    def test_save_product_success(self):
       # verification of the saved product
        url = reverse("food_selection:save_products")
        response = self.client.post(url, {"product_id": self.product.product_id})

        self.product.refresh_from_db()
        self.assertTrue(self.product.saved)  # must be True
        self.assertRedirects(response, "/saved_products_list/")  # redirection OK

    def test_save_product_does_not_exist(self):
        # Invalid ID during backup
        url = reverse("food_selection:save_products")
        response = self.client.post(url, {"product_id": '9999'})  # non-existent

        # We check that it redirects anyway.
        self.assertRedirects(response, "/saved_products_list/")
        # And that the existing product remains unchanged
        self.product.refresh_from_db()
        self.assertFalse(self.product.saved)
