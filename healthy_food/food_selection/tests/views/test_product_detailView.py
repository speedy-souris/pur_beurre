from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product

class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Pâtes complètes",
            product_id="123456",
            nutriscore="A",
            nutriments={"sugars_100g": 5, "salt_100g": 0.01},
            url="http://example.com",
            image_url="http://example.com/image.jpg",
        )

    def test_product_detail_view_status_code(self):
        url = reverse("food_selection:product", args=[self.product.product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_context(self):
        url = reverse("food_selection:product", args=[self.product.product_id])
        response = self.client.get(url)

        self.assertIn("product", response.context)
        self.assertEqual(response.context["product"], self.product)
        self.assertIn("nutriments", response.context)
        self.assertEqual(response.context["nutriments"], self.product.nutriments)
        self.assertIn("search_form", response.context)
