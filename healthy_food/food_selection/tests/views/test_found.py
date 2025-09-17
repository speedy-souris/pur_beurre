from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product, Category


class FoundViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Crée les données une seule fois pour toute la classe de test.
        """
        # --- Categories ---
        cls.cat_plats = Category.objects.create(name="Plats Préparés")
        cls.cat_snacks = Category.objects.create(name="Snacks")
        cls.cat_sucre = Category.objects.create(name="Sucré")
        cls.cat_boissons = Category.objects.create(name="Boissons")

        # --- Basic product for research ---
        # Note: str-type pk are used to match the probable model.
        cls.produit_recherche_d = Product.objects.create(name="Plat D", nutriscore="D", pk='1')
        cls.produit_recherche_d.categories.add(cls.cat_plats)

        # --- Valid substitutes for “Plat D” ---
        cls.substitut_plat_a = Product.objects.create(name="Plat Sain A", nutriscore="A", pk='2')
        cls.substitut_plat_a.categories.add(cls.cat_plats)
        cls.substitut_plat_b = Product.objects.create(name="Plat Mieux B", nutriscore="B", pk='3')
        cls.substitut_plat_b.categories.add(cls.cat_plats)

        # --- Irrelevant product (wrong category) ---
        cls.produit_non_pertinent = Product.objects.create(name="Boisson A", nutriscore="A", pk='4')
        cls.produit_non_pertinent.categories.add(cls.cat_boissons)

        # --- Scenario for the duplication test ---
        cls.produit_multi_cat = Product.objects.create(name="Snack Sucré D", nutriscore="D", pk='10')
        cls.produit_multi_cat.categories.add(cls.cat_snacks, cls.cat_sucre)
        cls.substitut_polyvalent_a = Product.objects.create(name="Snack Sain A", nutriscore="A", pk='11')
        cls.substitut_polyvalent_a.categories.add(cls.cat_snacks, cls.cat_sucre)
        cls.substitut_simple_b = Product.objects.create(name="Autre Snack B", nutriscore="B", pk='12')
        cls.substitut_simple_b.categories.add(cls.cat_snacks)

    def test_found_view_substitution_logic(self):
        """
        Tests whether the view returns only relevant substitutes.
        """
        response = self.client.get(reverse('food_selection:found'), {'product': self.produit_recherche_d.name})
        self.assertEqual(response.status_code, 200)

        alternative_products = response.context['products']

        self.assertEqual(len(alternative_products), 2)

        # CORRECTION: PKs are converted to integers for reliable comparison.
        actual_pks = {int(product.pk) for product in alternative_products}
        expected_pks = {int(self.substitut_plat_a.pk), int(self.substitut_plat_b.pk)}
        self.assertEqual(actual_pks, expected_pks)

    def test_substitute_with_common_category_is_unique(self):
        """
        Verify that a substitute sharing multiple categories appears only once.
        """
        response = self.client.get(reverse('food_selection:found'), {'product': self.produit_multi_cat.name})
        self.assertEqual(response.status_code, 200)

        alternative_products = response.context['products']

        # This test will fail (e.g., 3 != 2) until you add .distinct() to your view.
        self.assertEqual(len(alternative_products), 2)

        # CORRECTION: We are abandoning the .count() test and using PK comparison, which is more reliable.
        actual_pks = {int(product.pk) for product in alternative_products}
        expected_pks = {int(self.substitut_polyvalent_a.pk), int(self.substitut_simple_b.pk)}
        self.assertEqual(actual_pks, expected_pks)
