from django.core.management.base import BaseCommand
from food_selection.models import Product, Category


class Command(BaseCommand):
    help = 'registering products from the openfoodfact site to the database '

    def create_categories(self, all_categories):
        for category in all_categories:
            try:
                Category.objects.get(name=category)
            except Category.DoesNotExist:
                Category.objects.bulk_create([Category(name=category)])
            self.stdout.write('la categorie existe deja')

    def create_products(self, products):
        for index in range(len(products)):
            for nutriscore in products[index]['nutriscore']:
                try:
                    Product.objects.get(name=products[index]['name'])
                except Product.DoesNotExist:
                    Product.objects.bulk_create([Product(name=products[index]['name'], nutriscore=nutriscore)])
                self.stdout.write('le produit existe deja')

    @staticmethod
    def create_relation_categories_products(products):
        for index in range(len(products)):
            name_product = Product.objects.get(name=products[index]['name'])
            for category in products[index]['categories']:
                name_category = Category.objects.get(name=category)
                name_product.categories.add(name_category)

    def handle(self, *args, **options):
        product = {'name': 'coquilette',
                   'categories': {"Aliments et boissons à base de végétaux",
                                 "Aliments d'origine végétale", "Céréales et pommes de terre",
                                 "Céréales et dérivés", "Pâtes alimentaires", "Pâtes alimentaires de céréales",
                                 "Pâtes sèches", "Pâtes de blé dur", "Coquillettes", "Coquillettes de blé dur"},
                   'nutriscore': 'C'}

        product2 = {'name': 'spagetti',
                    'categories': {"Aliments et boissons à base de végétaux",
                                  "Aliments d'origine végétale",
                                  "Céréales et pommes de terre",
                                  "Céréales et dérivés", "Pâtes alimentaires",
                                  "Pâtes alimentaires de céréales", "Pâtes sèches",
                                  "Pâtes de blé dur", "Spaghetti", "Spaghettis de blé dur"},
                    'nutriscore': 'A'}

        products = [product, product2]
        all_categories = [categories for categories in products for categories in categories['categories']]

        # create categories
        self.create_categories(all_categories)
        # create products
        self.create_products(products)
        # add relation categories with products
        self.create_relation_categories_products(products)


