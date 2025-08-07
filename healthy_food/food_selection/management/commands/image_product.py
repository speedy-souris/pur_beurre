from django.core.management.base import BaseCommand
from food_selection.models import Product
import requests
import os

class Command(BaseCommand):
    help = 'Télécharge les images des produits et les stocke localement.'

    def handle(self, *args, **options):
        products = Product.objects.all()
        counter = 0
        images_folder_path = "food_selection/static/food_selection/images/image_product"

        # Création du dossier s'il n'existe pas
        if not os.path.exists(images_folder_path):
            os.makedirs(images_folder_path)

        for product in products:
            counter += 1

            if counter % max(1, len(products) // 50) == 0:
                print(f"Téléchargement en cours... {counter}/{len(products)} produits traités")

            image_product_id = product.product_id
            image_file_path = os.path.join(images_folder_path, f"{image_product_id}.jpg")

            # Ne pas re-télécharger si l'image existe déjà
            if os.path.exists(image_file_path):
                continue

            image_url = product.image_url

            # Vérification de l'URL
            if not image_url or not isinstance(image_url, str) or not image_url.startswith("http"):
                print(f"URL invalide pour le produit {product.product_id} : {image_url or 'N/A'}")
                continue

            try:
                response = requests.get(image_url, timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération de l'image pour {product.product_id} : {e}")
                continue

            if response.status_code == 200 and response.content:
                with open(image_file_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Image non disponible pour le produit {product.product_id} (status {response.status_code})")
