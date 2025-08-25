from django.core.management.base import BaseCommand
from food_selection.models import Product


class Command(BaseCommand):
    help = 'deleting image from the static files'

    def handle(self, *args, **options):
        all_products_db = Product.objects.all()
        for product in all_products_db:
            print(f"effacement de {product.product_id}.jpg")

