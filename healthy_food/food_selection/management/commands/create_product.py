from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import json
import requests


class Command(BaseCommand):
    help = 'registering products from the openfoodfact site to the database '

    def create_categories(self, all_categories):
        for category in all_categories:
            try:
                Category.objects.get(name=category)
            except Category.DoesNotExist:
                Category.objects.bulk_create([Category(name=category)])
            else:
                self.stdout.write('la categorie existe deja')

    def create_products(self, products):
        for p in products:
            if len(p['nutriscore']) > 1: # exempple nutriscore = 'NOT-APPLICABLE'
                continue
            try:
                Product.objects.get(name=p['name'])
            except Product.DoesNotExist:
                Product.objects.bulk_create([Product(name=p['name'], nutriscore=p['nutriscore'])])
            else:
                self.stdout.write('le produit existe deja')

    # def create_products(self, products):
    #     for index in range(len(products)):
    #         for nutriscore in products[index]['nutriscore']:
    #             try:
    #                 Product.objects.get(name=products[index]['name'])
    #             except Product.DoesNotExist:
    #                 Product.objects.bulk_create([Product(name=products[index]['name'], nutriscore=nutriscore)])
    #             self.stdout.write('le produit existe deja')

    @staticmethod
    def create_relation_categories_products(products):
        name_product = ''
        for index in range(len(products)):
            try:
                name_product = Product.objects.get(name=products[index]['name'])
            except Product.DoesNotExist:
                print("Le produit n'existe pas")
            else:
                for category in products[index]['categories']:
                    name_category = Category.objects.get(name=category)
                    name_product.categories.add(name_category)

    def handle(self, *args, **options):
        data = ''
        products = []
        categories_list = ['Pâtes alimentaires de céréales', 'Boissons', 'Mélanges de légumes frais']
        # URL produit openfoodfacts
        for category in categories_list:
            url = f"https://fr.openfoodfacts.org/api/v2/search?categories_tags_fr={category}"\
                  "&fields=product_name,nutriscore_grade,categories&page=100&page_size=100"
            # product infos
            product_infos = requests.get(url)
            print(product_infos.status_code)
            data = json.loads(product_infos.text)

            for index in range(len(data['products'])):
                product3 = {'name': data['products'][index]['product_name'],
                            'categories': data['products'][index]['categories'].split(', '),
                            'nutriscore': data['products'][index]['nutriscore_grade'].upper()}
                products.append(product3)
                all_categories = [categories for categories in products for categories in categories['categories']]

                # create categories
                self.create_categories(all_categories)
                # create products
                self.create_products(products)
                # add relation categories with products
                self.create_relation_categories_products(products)


