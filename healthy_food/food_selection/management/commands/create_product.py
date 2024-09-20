from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import json
import requests


class Command(BaseCommand):
    help = 'registering products from the openfoodfact site to the database '

    @staticmethod
    def create_categories(all_categories):
        categories = set()
        for category in all_categories:
            try:
                Category.objects.get(name=category)
            except Category.DoesNotExist:
                categories.add(Category(name=category))
            else:
                # self.stdout.write('la categorie existe deja')
                pass
        Category.objects.bulk_create(categories)

    @staticmethod
    def create_products(products):
        products_lst = set()
        for product in products:
            if len(product['nutriscore']) > 1:  # exempple nutriscore = 'NOT-APPLICABLE'
                continue
            try:
                Product.objects.get(product_id=product['product_id'])
            except Product.DoesNotExist:
                products_lst.add(Product(name=product ['name'],
                                         product_id=product['product_id'],
                                         nutriscore=product['nutriscore'],
                                         url=product['url']))
            else:
                # self.stdout.write('le produit existe deja')
                pass
        Product.objects.bulk_create(products_lst)

    @staticmethod
    def create_relation_categories_products(products):
        for product_as_json in products:
            try:
                product_as_object = Product.objects.get(product_id=product_as_json['product_id'])
            except Product.DoesNotExist:
                # print("Le produit n'existe pas")
                pass
            else:
                for category in product_as_json['categories']:
                    name_category = Category.objects.get(name=category)
                    print(f'produit = {product_as_json}')
                    product_as_object.categories.add(name_category)

    def handle(self, *args, **options):
        image = ''
        products = []
        categories_list = {'Pâtes alimentaires de céréales', 'Boissons'}
                           #'Mélanges de légumes frais', 'fruits secs', 'poissons',
                           #'biscottes', 'patisseries', 'fromages', 'charcuteries', 'confitures'}
        counter = 1
        # URL produit openfoodfacts
        for category in categories_list:
            url = f"https://fr.openfoodfacts.org/api/v1/search?categories_tags_fr={category}"\
                   "&fields=code,product_name_fr,nutriscore_grade,categories_tags_fr,url,image_url&page=1&page_size=100"            # product infos
            product_infos = requests.get(url)
            print(product_infos.status_code)
            data = json.loads(product_infos.text)
            for product in data['products']:
                try:
                    if product['product_name_fr'] == '':
                        continue
                except KeyError:
                    continue
                else:
                    name = product['product_name_fr']
                print()
                print(counter)
                print(f'name = {name}')
                print()
                print(product['code'])
                # image_product_infos = requests.get(product['image_url'])
                # if  image_product_infos.status_code == 200:
                #     f = open("food_selection/static/food_selection/images/image.jpg", "wb")
                #     f.write(image_product_infos.content)
                #     f.close()
                product3 = {
                            'name': name,
                            'categories': product['categories_tags_fr'],
                            'nutriscore': product['nutriscore_grade'].upper(),
                            'url': product['url'],
                            'product_id': product['code']
                            # 'image': product['image_url']
                            }
                products.append(product3)
                print(f'produit final : {products[-1]}')
                counter += 1
        all_categories = [categories for categories in products for categories in categories['categories']]
        # create categories
        self.create_categories(all_categories)
        # create products
        self.create_products(products)
        # add relation categories with products
        self.create_relation_categories_products(products)
