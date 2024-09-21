from django.core.management.base import BaseCommand
from food_selection.models import Product, Category


class Command(BaseCommand):
    help = 'deleting data from the database'

    def delete_products(self, all_products_db):
        for product_as_object in all_products_db:
            try:
                product_as_object.delete()
            except TypeError:
                self.stdout.write("le produit n'existe pas")

    def delete_categories(self, all_categories_db):
        for category_as_object in all_categories_db:
            try:
                category_as_object.delete()
            except TypeError:
                self.stdout.write("la vategorie n'existe pas")

    def handle(self, *args, **options):
        all_products_db = Product.objects.all()
        print(f'effacement de {len(all_products_db)} produits')
        self.delete_products(all_products_db)
        all_categories_db = Category.objects.all()
        print(f'effacement de {len(all_categories_db)} categories')
        self.delete_categories(all_categories_db)