from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup
from food_selection.models import Product, Category, Favorite


class SavedTemplateWithFavoritesTest(TestCase):
    """
       Vérifie le nombre de produits enregistrés en favoris.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Crée les données initiales pour les tests de produits enregistrés
        """
        User = get_user_model()
        # user creation
        cls.user = User.objects.create_user(username='testuser', password='password')

        # 1. Création des catégories
        category_confiture = Category.objects.create(name="Confitures")
        category_pate_a_tartiner = Category.objects.create(name="Pâtes à tartiner")
        # 2. Création de 7 produits favoris pour tester la pagination qui est de 6 produits par page
        for i in range(7):
            favorites_product = Product.objects.create(
                product_id=f"0000{i}",
                name=f"Confiture Allégée {i + 1}",
                nutriscore="a"
            )
            favorites_product.categories.add(category_confiture, category_pate_a_tartiner)

            Favorite.objects.create(user=cls.user, product=favorites_product)

    def setUp(self):
        self.client.force_login(self.user)

    def test_count_favorites_products_on_page(self):
        """
        Vérifie que la page affiche bien 6 produits en favoris (la limite par page).
        """
        # Étape 1: Simuler la requête GET de l'utilisateur
        response = self.client.get(reverse('food_selection:saved-list'))

        # Étape 2: Vérifications du bon template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/saved_products.html')

        # Étape 3: response.content contient le HTML brut de la page rendue
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Compter les éléments qui correspondent à un produit favoris
        favorites_products_divs = soup.select('div.favorite_saved_products')
        # Étape 5: Affirmer que le nombre d'éléments trouvés est bien 6
        self.assertEqual(len(favorites_products_divs), 6)

    def test_count_favorite_products_on_page2(self):
        """
        Vérifie que la page affiche bien 1 produits en favoris.
        """
        # Étape 1: Simuler la requête GET de l'utilisateur
        response = self.client.get(reverse('food_selection:saved-list'), {'page': 2})
        # Étape 2: Vérifications du bon template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_selection/saved_products.html')

        # Étape 3: response.content contient le HTML brut de la page rendue
        soup = BeautifulSoup(response.content, 'html.parser')
        # Étape 4: Compter les éléments qui correspondent à un produit en favoris
        favorite_products_divs = soup.select('div.favorite_saved_products')
        # Étape 5: Affirmer que le nombre d'éléments trouvés est bien 1
        self.assertEqual(len(favorite_products_divs), 1)