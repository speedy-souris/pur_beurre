from django.core.management.base import BaseCommand
from food_selection.models import Product, Category


class Command(BaseCommand):
    help = 'deleting image from the static files'

    def handle(self, *args, **options):
        all_products_db = Product.objects.all()
        for product_id in all_products_db:
            print(f"effacement de {product_id.product_id}.jpg")
