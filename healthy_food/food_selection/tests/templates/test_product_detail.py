from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from food_selection.models import Product


class ProductDetailViewTest(TestCase):
    """
    Series of tests for the view and template displaying product details.
    """

    @classmethod
    def setUpTestData(cls):
        """
        This method is executed only once for the test class.
        We create a dummy product for our tests..
        """
        cls.product = Product.objects.create(
            product_id='12345',
            name='Super Biscuit',
            nutriscore='A',
            url='http://example.com/biscuit',
            nutriments={
                'energy_100g': 450,
                'proteins_100g': 8.5,
                'carbohydrates_100g': 60.2,
                'sugars_100g': 25.1,
                'fiber_100g': 3.2,
                'salt_100g': '?',
                'fat_100g': 20.0,
                'saturated_fat_100g': 9.8
            }
        )

    def setUp(self):
        """
        This method is executed before each test.
        We perform a GET request on the product detail page.
        """
        # Replace ‘product-detail’ with the name of your URL.
        url = reverse('food_selection:product', args=[self.product.product_id])
        self.response = self.client.get(url)
        # We use BeautifulSoup to parse the HTML content of the response.
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_page_title_is_correct(self):
        """
        Check that the template title is correct.
        """
        # the template title == page_name
        expected_title = 'Détails du produit'
        # We search for the <title> tag in the HTML.
        page_title = self.soup.find('title')

        self.assertIsNotNone(page_title, "Pas de Titre")
        self.assertEqual(page_title.string, expected_title, "titre inconnu")

    def test_view_uses_the_correct_template(self):
        """
        Verify that the view uses the correct template file.
        """
        self.assertTemplateUsed(self.response, 'food_selection/product_detail.html')

    def test_the_page_contains_general_product_information(self):
        """
        Check that the name, product image, and Nutri-Score are present.
        """
        # Verify that the title (h1) contains the product name.
        titre_h1 = self.soup.find('h1', class_='card-title')
        self.assertIsNotNone(titre_h1, "La balise h1 avec la classe 'card-title' est manquante.")
        self.assertEqual(titre_h1.string.strip(), self.product.name)

        # Verify that the main product image is correct.
        image_produit = self.soup.find('img', class_='card-img-top')
        self.assertIsNotNone(image_produit, "L'image principale du produit est manquante.")
        # We verify that part of the image path is correct.
        self.assertIn(f'images/image_product/{self.product.product_id}.jpg', image_produit['src'])

        # Check that the Nutri-Score image is correct.
        image_nutriscore = self.soup.find('img', alt="nutriscore du produit selectionné")
        self.assertIsNotNone(image_nutriscore, "L'image du Nutri-Score est manquante.")
        self.assertIn(f'images/image_nutriscore/Nutriscore_{self.product.nutriscore}.jpg', image_nutriscore['src'])

    def test_the_nutrition_table_contains_the_correct_values(self):
        """
        Check that the values in the nutrition table are correct.
        """
        # We are looking for the painting
        table = self.soup.find('table', class_='table')
        self.assertIsNotNone(table, "Le tableau des informations nutritionnelles est manquant.")

        # We retrieve all the rows from the table body (tbody).
        lignes = table.find('tbody').find_all('tr')

        # Dictionary of expected values for easy verification
        valeurs_attendues = {
            'Énergie': "450 kcal",
            'Protéines': "8,5 g",
            'Glucides': "60,2 g",
            'Dont sucres': "25,1 g",
            'Fibres': "3,2 g",
            'Sel': f"? g",
            'Matières grasses': "20,0 g",
            'Dont acides gras saturés': "9,8 g",
        }

        # We go through each row of the table to check its contents.
        for ligne in lignes:
            cellules = ligne.find_all('td')
            nom_nutriment = cellules[0].string.strip()
            valeur_nutriment = cellules[1].string.strip()

            self.assertIn(nom_nutriment, valeurs_attendues, f"Le nutriment '{nom_nutriment}' ne devrait pas être dans le tableau.")
            self.assertEqual(valeur_nutriment, valeurs_attendues[nom_nutriment], f"La valeur pour '{nom_nutriment}' est incorrecte.")

    def test_the_link_to_openfoodfacts_is_correct(self):
        """
        Check that the link to the OpenFoodFacts product page is present and correct.
        """
        lien = self.soup.find('a', class_='btn-primary')
        self.assertIsNotNone(lien, "Le lien vers OpenFoodFacts est manquant.")
        self.assertEqual(lien['href'], self.product.url)
        self.assertEqual(lien.string.strip(), 'Fiche Produit OpenFoodFacts')
        self.assertIn('target', lien.attrs)
        self.assertEqual(lien['target'], '_blank')