from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from food_selection.models import Product


class ProductDetailViewTest(TestCase):
    """
    Série de tests pour la vue et le template affichant les détails d'un produit.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Cette méthode est exécutée une seule fois pour la classe de test.
        Nous créons un produit factice pour nos tests.
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
        Cette méthode est exécutée avant chaque test.
        Nous effectuons une requête GET sur la page de détail du produit.
        """
        # Remplacez 'product-detail' par le nom de votre URL
        url = reverse('food_selection:product', args=[self.product.product_id])
        self.response = self.client.get(url)
        # Nous utilisons BeautifulSoup pour analyser le contenu HTML de la réponse
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def test_page_title_is_correct(self):
        """
        Vérifie que le titre du template.
        """
        # le titre du template == page_name
        expected_title = 'Détails du produit'
        # On recherche la balise <title> dans le HTML.
        page_title = self.soup.find('title')

        self.assertIsNotNone(page_title, "Pas de Titre")
        self.assertEqual(page_title.string, expected_title, "titre inconnu")

    def test_view_uses_the_correct_template(self):
        """
        Vérifie que la vue utilise le bon fichier de template.
        """
        self.assertTemplateUsed(self.response, 'food_selection/product_detail.html') # Adaptez le chemin

    def test_the_page_contains_general_product_information(self):
        """
        Vérifie la présence du nom, de l'image du produit et du Nutri-Score.
        """
        # Vérifie que le titre (h1) contient le nom du produit
        titre_h1 = self.soup.find('h1', class_='card-title')
        self.assertIsNotNone(titre_h1, "La balise h1 avec la classe 'card-title' est manquante.")
        self.assertEqual(titre_h1.string.strip(), self.product.name)

        # Vérifie que l'image principale du produit est correcte
        image_produit = self.soup.find('img', class_='card-img-top')
        self.assertIsNotNone(image_produit, "L'image principale du produit est manquante.")
        # On vérifie qu'une partie du chemin de l'image est correcte
        self.assertIn(f'images/image_product/{self.product.product_id}.jpg', image_produit['src'])

        # Vérifie que l'image du Nutri-Score est correcte
        image_nutriscore = self.soup.find('img', alt="nutriscore du produit selectionné")
        self.assertIsNotNone(image_nutriscore, "L'image du Nutri-Score est manquante.")
        self.assertIn(f'images/image_nutriscore/Nutriscore_{self.product.nutriscore}.jpg', image_nutriscore['src'])

    def test_the_nutrition_table_contains_the_correct_values(self):
        """
        Vérifie que les valeurs dans le tableau nutritionnel sont correctes.
        """
        # On recherche le tableau
        table = self.soup.find('table', class_='table')
        self.assertIsNotNone(table, "Le tableau des informations nutritionnelles est manquant.")

        # On récupère toutes les lignes du corps du tableau (tbody)
        lignes = table.find('tbody').find_all('tr')

        # Dictionnaire des valeurs attendues pour une vérification facile
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

        # On parcourt chaque ligne du tableau pour vérifier son contenu
        for ligne in lignes:
            cellules = ligne.find_all('td')
            nom_nutriment = cellules[0].string.strip()
            valeur_nutriment = cellules[1].string.strip()

            self.assertIn(nom_nutriment, valeurs_attendues, f"Le nutriment '{nom_nutriment}' ne devrait pas être dans le tableau.")
            self.assertEqual(valeur_nutriment, valeurs_attendues[nom_nutriment], f"La valeur pour '{nom_nutriment}' est incorrecte.")

    def test_the_link_to_openfoodfacts_is_correct(self):
        """
        Vérifie que le lien vers la fiche produit OpenFoodFacts est présent et correct.
        """
        lien = self.soup.find('a', class_='btn-primary')
        self.assertIsNotNone(lien, "Le lien vers OpenFoodFacts est manquant.")
        self.assertEqual(lien['href'], self.product.url)
        self.assertEqual(lien.string.strip(), 'Fiche Produit OpenFoodFacts')
        self.assertIn('target', lien.attrs)
        self.assertEqual(lien['target'], '_blank')