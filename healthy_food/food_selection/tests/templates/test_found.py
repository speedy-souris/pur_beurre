from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup
from food_selection.models import Product, Category


class EmptyDBFoundTemplateTest(TestCase):
    """
    Tests whether the template returns only relevant substitutes.
    """
    def test_found_template_substitution_logic(self):
        response = self.client.get(reverse('food_selection:found'), {'product': 'confiture de fraise'})
        self.assertEqual(response.status_code, 200)

        # Vérifie que le template spécifié a été utilisé pour rendre la page
        self.assertTemplateUsed(response, 'food_selection/products.html')

class FoundTemplateWithSubstitutesTest(TestCase):
    """
       Vérifie le nombre de substituts affichés en utilisant BeautifulSoup.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Crée les données initiales pour les tests
        """
        # 1. Création des catégories
        category_confiture = Category.objects.create(name="Confitures")
        category_pate_a_tartiner = Category.objects.create(name="Pâtes à tartiner")

        # 2. Création du produit qui sera recherché (avec un mauvais Nutri-Score)
        cls.product_to_find = Product.objects.create(
            product_id="3017620422003",
            name="Confiture de Fraise Classique",
            nutriscore="d"
        )
        cls.product_to_find.categories.add(category_confiture)

        # 3. Création de 7 produits de substitution pour tester la pagination qui est de 6 produits par page
        for i in range(7):
            product = Product.objects.create(
                product_id=f"0000{i}",
                name=f"Confiture Allégée {i+1}",
                nutriscore="a"
            )
            product.categories.add(category_confiture, category_pate_a_tartiner)

    def test_count_substitute_products_on_page(self):
        """
        Vérifie que la page affiche bien 6 produits de substitution (la limite par page).
        """
        # Étape 1: Simuler la requête GET de l'utilisateur
        response = self.client.get(reverse('food_selection:found'), {'product': self.product_to_find.name})

        # Étape 2: Vérifications du bon template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/products.html')

        # Étape 3: response.content contient le HTML brut de la page rendue
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Compter les éléments qui correspondent à un produit de substitution
        substitute_products_divs = soup.select('div.substitute_products')
        # Étape 5: Affirmer que le nombre d'éléments trouvés est bien 6
        self.assertEqual(len(substitute_products_divs), 6)

    def test_count_substitute_products_on_page2(self):
        """
        Vérifie que la page affiche bien 6 produits de substitution (la limite par page).
        """
        # Étape 1: Simuler la requête GET de l'utilisateur
        response = self.client.get(reverse('food_selection:found'), {'product': self.product_to_find.name,
                                                                     'page': 2})
        # Étape 2: Vérifications du bon template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/products.html')

        # Étape 3: response.content contient le HTML brut de la page rendue
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Compter les éléments qui correspondent à un produit de substitution
        substitute_products_divs = soup.select('div.substitute_products')
        # Étape 5: Affirmer que le nombre d'éléments trouvés est bien 1
        self.assertEqual(len(substitute_products_divs), 1)