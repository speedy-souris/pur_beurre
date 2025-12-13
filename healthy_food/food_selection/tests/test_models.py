from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from food_selection.models import Product, Favorite, Category

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
        )

    def test_product_creation(self):
        # created product
        product = Product.objects.get(product_id=123456)
        self.assertEqual(product.name, "Chips")
        self.assertEqual(product.nutriscore, "E")

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
            )


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Snacks")

    def test_category_creation(self):
        # Verify that the category has been created
        self.assertEqual(self.category.name, "Snacks")
        self.assertTrue(isinstance(self.category, Category))

    def test_str_method(self):
        # Verify that __str__ returns the name
        self.assertEqual(str(self.category), "Snacks")

    def test_unique_name_constraint(self):
        # Verify that two categories cannot be created with the same name
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Snacks")  # same PK ==> error

class FavoriteModelTest(TestCase):

    def setUp(self):
        """
        On doit créer un utilisateur, un produit pour tous les tests
        """
        User = get_user_model()
        self.user = User.objects.create_user('testuser', password='password')

        self.product = Product.objects.create(
            product_id="123456789",
            name="biscottes",
            nutriscore="e"
        )

    def test_favorite_creation_and_str(self):
        """
        Test 1: Vérifie la création normale et la méthode __str__
        """
        favorite = Favorite.objects.create(user=self.user, product=self.product)

        # Vérifie que l'objet est bien créé
        self.assertTrue(isinstance(favorite, Favorite))
        self.assertIsNotNone(favorite.created_at)

        expected_str = f"{self.user.username} aime le produit {self.product.name}"
        self.assertEqual(str(favorite), expected_str)

    def test_unique_together_constraint(self):
        """
        Test 2: Vérifie qu'on ne peut pas avoir de doublons (Même User + Même Produit)
        """
        # 1. On crée le premier favori
        Favorite.objects.create(user=self.user, product=self.product)

        # 2. On essaie de créer EXACTEMENT le même favori
        # Cela doit lever une erreur d'intégrité (IntegrityError) au niveau de la base de données
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(user=self.user, product=self.product)

    def test_cascade_delete_user(self):
        """
        Test 3: Si l'utilisateur est supprimé, le favori doit disparaître
        """
        Favorite.objects.create(user=self.user, product=self.product)

        # Vérification pré-suppression
        self.assertEqual(Favorite.objects.count(), 1)

        # Action : Suppression de l'utilisateur
        self.user.delete()

        # Vérification : Le favori doit avoir été supprimé automatiquement
        self.assertEqual(Favorite.objects.count(), 0)

    def test_cascade_delete_product(self):
        """
        Test 4: Si le produit est supprimé, le favori doit disparaître
        """
        Favorite.objects.create(user=self.user, product=self.product)

        # Vérification pré-suppression
        self.assertEqual(Favorite.objects.count(), 1)

        # Action : Suppression du produit
        self.product.delete()

        # Vérification : Le favori doit avoir été supprimé
        self.assertEqual(Favorite.objects.count(), 0)