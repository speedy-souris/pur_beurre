from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import json
import requests


class Command(BaseCommand):
    help = 'registering products from the openfoodfact site to the database '

    @staticmethod
    def create_categories(self, all_categories):
        for category in all_categories:
            try:
                Category.objects.get(name=category)
            except Category.DoesNotExist:
                Category.objects.bulk_create([Category(name=category)])
            else:
                # self.stdout.write('la categorie existe deja')
                pass

    @staticmethod
    def create_products(self, products):
        for product in products:
            if len(product['nutriscore']) > 1:  # exempple nutriscore = 'NOT-APPLICABLE'
                continue
            try:
                Product.objects.get(name=product['name'])
            except Product.DoesNotExist:
                Product.objects.bulk_create([Product(name=product['name'],
                                                     nutriscore=product['nutriscore'],
                                                     url=product['url'])])
            else:
                # self.stdout.write('le produit existe deja')
                pass

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
        for product in products:
            try:
                name_product = Product.objects.get(name=product['name'])
            except Product.DoesNotExist:
                # print("Le produit n'existe pas")
                pass
            else:
                for category in product['categories']:
                    name_category = Category.objects.get(name=category)
                    name_product.categories.add(name_category)

    def handle(self, *args, **options):
        products = []
        categories_list = ['Pâtes alimentaires de céréales', 'Boissons', 'Mélanges de légumes frais']
        # URL produit openfoodfacts
        for category in categories_list:
            #  url = f"https://fr.openfoodfacts.org/api/v2/search?categories_tags_fr={category}"\
                  #  "&fields=product_name_fr,nutriscore_grade,categories,url&page=1&page_size=100"
            url = f"https://fr.openfoodfacts.org/api/v2/search?categories_tags_fr={category}"\
                    "&fields=product_name_fr,nutriscore_grade,categories_tags_fr,url&page=1&page_size=100"
            # product infos
            product_infos = requests.get(url)
            print(product_infos.status_code)
            data = json.loads(product_infos.text)
            print(f'data = {data}')
            print()
            for product in data['products']:
                print(f'produits = {product}')
                try:
                    product3 = {'name': product['product_name_fr'],
                        'categories': product['categories_tags_fr'].split(', '),
                        'nutriscore': product['nutriscore_grade'].upper(),
                        'url': product['url']}
                except (AttributeError, KeyError):
                    continue
                else:
                    products.append(product3)
                    print(f'produit final : {products}')
                    #  print(f'nom : {products["name"]} - url : {products["url"]}')
                    all_categories = [categories for categories in products for categories in categories['categories_tags_fr']]
                    # create categories
                    self.create_categories(all_categories)
                    # create products
                    self.create_products(products)
                    # add relation categories with products
                    self.create_relation_categories_products(products)



