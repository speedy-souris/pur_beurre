from django.test import TestCase
from django.db import IntegrityError
from food_selection.models import Product, Category

class ProductModelTest(TestCase):

    def setUp(self):
        # creation of categories
        self.category1 = Category.objects.create(name="Snacks")
        self.category2 = Category.objects.create(name="Aperitif")
        # creation of Product
        self.product = Product.objects.create(
            name="Chips",
            nutriscore="E",
            product_id=123456,
            nutriments={"sugars_100g": 1.0, "salt_100g": 2.0},
            url = "https://example.com/chips",
            image_url = "https://example.com/chips.jpg",
            saved = True
        )

    def test_product_creation(self):
        # created product
        product = Product.objects.get(product_id=123456)
        self.assertEqual(product.name, "Chips")
        self.assertEqual(product.nutriscore, "E")
        # saved product
        self.assertTrue(product.saved)

    def test_product_nutriments(self):
        # nutritional value
        self.assertEqual(self.product.nutriments["salt_100g"], 2.0)
        self.assertEqual(self.product.nutriments["sugars_100g"], 1.0)

    def test_product_categories(self):
        # multiple categories ==> ManyToMany
        self.product.categories.add(self.category1, self.category2)
        # Categories present in the ManyToMany relationship
        categories = self.product.categories.all()
        self.assertEqual(categories.count(), 2)
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

    def test_product_id_uniqueness(self):
        # creation of product with existing product_id ==> unique product_id
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Biscuits",
                nutriscore="B",
                product_id=123456,
                nutriments={"fat_100g": 8, "sugars_100g": 12},
                url="https://example.com/biscuits",
                image_url="https://example.com/biscuits.jpg",
                saved=False
            )