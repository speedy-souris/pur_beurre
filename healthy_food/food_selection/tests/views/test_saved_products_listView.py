from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product

class SavedProductsListViewTest(TestCase):
    def setUp(self):
        # Produit sauvegardé
        self.saved_product = Product.objects.create(
            name="Riz complet",
            product_id="111111",
            nutriscore="A",
            nutriments={"sugars_100g": 1, "salt_100g": 0.01},
            url="http://example.com/riz",
            image_url="http://example.com/riz.jpg",
            saved=True,
        )

        # Produit NON sauvegardé
        self.unsaved_product = Product.objects.create(
            name="Chips",
            product_id="222222",
            nutriscore="E",
            nutriments={"sugars_100g": 15, "salt_100g": 2},
            url="http://example.com/chips",
            image_url="http://example.com/chips.jpg",
            saved=False,
        )

    def test_only_saved_products_listed(self):
        """
        Vérifie que seuls les produits avec saved=True apparaissent
        """
        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Riz complet")   # doit apparaître
        self.assertNotContains(response, "Chips")      # ne doit PAS apparaître

    def test_context_contains_expected_keys(self):
        """
        Vérifie que le contexte contient search_form, page_obj et page_name
        """
        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        self.assertIn("search_form", response.context)
        self.assertIn("page_obj", response.context)
        self.assertEqual(response.context["page_name"], "Mes Favoris")

    def test_pagination_limit(self):
        """
        Vérifie que la pagination limite à 6 produits par page
        """
        # On crée 12 produits sauvegardés
        for i in range(12):
            Product.objects.create(
                name=f"Produit {i}",
                product_id=f"p{i}",
                nutriscore="B",
                nutriments={},
                url=f"http://example.com/{i}",
                image_url=f"http://example.com/{i}.jpg",
                saved=True,
            )

        url = reverse("food_selection:saved-list")
        response = self.client.get(url)

        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 6)  # doit être limité à 6
        self.assertTrue(page_obj.has_next())  # doit avoir une 2ème page
