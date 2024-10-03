from django.core.management.base import BaseCommand
from food_selection.models import Product, Category


class Command(BaseCommand):
    help = 'deleting data from the database'

    def handle(self, *args, **options):
        all_products_db = Product.objects.all()
        print(f'effacement de {len(all_products_db)} produits')
        all_products_db.delete()
        all_categories_db = Category.objects.all()
        print(f'effacement de {len(all_categories_db)} categories')
        all_categories_db.delete()