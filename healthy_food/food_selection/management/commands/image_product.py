from django.core.management.base import BaseCommand
from django.conf import settings
from food_selection.models import Product
import os
import requests

class Command(BaseCommand):
    help = "Download the product images in static/food_selection/images/image_product"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        image_dir = os.path.join(settings.BASE_DIR, 'food_selection', 'static', 'food_selection', 'images', 'image_product')
        os.makedirs(image_dir, exist_ok=True)

        products = Product.objects.exclude(image_url__isnull=True)\
                                  .exclude(image_url__exact='')\
                                  .filter(image_url__startswith='http')

        if not silent:
            self.stdout.write(f"🔄 Démarrage du téléchargement de {products.count()} images produit...")

        for i, product in enumerate(products, 1):
            try:
                response = requests.get(product.image_url, timeout=10)
                response.raise_for_status()

                file_path = os.path.join(image_dir, f"{product.product_id}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                if not silent and i % 50 == 0:
                    self.stdout.write(f"✅ Images produit téléchargées : {i}/{products.count()}")

            except Exception as e:
                if not silent:
                    self.stderr.write(f"❌ Erreur téléchargement image produit {product.product_id} : {e}")

        if not silent:
            self.stdout.write(self.style.SUCCESS(f"✅ Téléchargement des images produit terminé, {products.count()} images traitées."))
