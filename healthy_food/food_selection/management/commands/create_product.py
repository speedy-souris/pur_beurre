from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import json
import requests


class Command(BaseCommand):
    help = 'Create product and categories for registering products from the openfoodfact site to the database '

    @staticmethod
    def create_categories(categories_as_final_json_list):
        categories_object_list = set()
        for category_as_json in categories_as_final_json_list:
            try:
                Category.objects.get(name=category_as_json)
            except Category.DoesNotExist:
                categories_object_list.add(Category(name=category_as_json))
            else:
                pass
        Category.objects.bulk_create(categories_object_list)

    @staticmethod
    def create_products(products_final_json_list):
        products_object_list = set()
        for product_as_json in products_final_json_list:
            if len(product_as_json['nutriscore']) > 1:  # exempple nutriscore = 'NOT-APPLICABLE'
                continue
            try:
                Product.objects.get(product_id=product_as_json['product_id'])
            except Product.DoesNotExist:
                products_object_list.add(Product(name=product_as_json['name'],
                                         product_id=product_as_json['product_id'],
                                         nutriscore=product_as_json['nutriscore'],
                                         url=product_as_json['url']),
                                         image=product_as_json['image_url'])
            else:
                # self.stdout.write('le produit existe deja')
                pass
        Product.objects.bulk_create(products_object_list)

    @staticmethod
    def create_relation_categories_products(products_final_json_list):
        for product_as_json in products_final_json_list:
            try:
                product_as_object = Product.objects.get(product_id=product_as_json['product_id'])
            except Product.DoesNotExist:
                # print("Le produit n'existe pas")
                pass
            else:
                for category_as_json in product_as_json['categories']:
                    category_as_object = Category.objects.get(name=category_as_json)
                    print(f'produit = {product_as_json}')
                    product_as_object.categories.add(category_as_object)

    def handle(self, *args, **options):
        image = ''
        products_final_json_list = []
        categories_object_list = ['Pâtes alimentaires de céréales', 'Boissons',
                           'Mélanges de légumes frais', 'fruits secs', 'poissons',
                           'biscottes', 'patisseries', 'fromages', 'charcuteries', 'confitures']
        counter = 1
        # URL product openfoodfacts
        for category_as_element in categories_object_list:
            url = f"https://fr.openfoodfacts.org/api/v1/search?categories_tags_fr={category_as_element}"\
                   "&fields=code,product_name_fr,nutriscore_grade,categories_tags_fr,url,image_url&page=1&page_size=100"
            # product infos
            product_infos = requests.get(url)
            print(product_infos.status_code)
            data_as_json = json.loads(product_infos.text)
            for product_as_object in data_as_json['products']:
                print(f"product_as_object = {product_as_object}")
                try:
                    if product_as_object['product_name_fr'] == '':
                        continue
                except KeyError:
                    continue
                else:
                    name_object = product_as_object['product_name_fr']
                print()
                print(counter)
                print(f'name = {name_object}')
                print()
                print(product_as_object['code'])
                # image_product_infos = requests.get(product['image_url'])
                # if  image_product_infos.status_code == 200:
                #     f = open("food_selection/static/food_selection/images/image.jpg", "wb")
                #     f.write(image_product_infos.content)
                #     f.close()
                create_final_product_object = {
                            'name': name_object,
                            'categories': product_as_object['categories_tags_fr'],
                            'nutriscore': product_as_object['nutriscore_grade'].upper(),
                            'url': product_as_object['url'],
                            'product_id': product_as_object['code'],
                            'image': product_as_object['image_url']
                            }
                products_final_json_list.append(create_final_product_object)
                print(f'produit final : {products_final_json_list[-1]}')
                counter += 1
        categories_as_final_json_list = [
                                         categories_as_element for categories_as_json in products_final_json_list
                                            for categories_as_element in categories_as_json['categories']]
        # create categories
        self.create_categories(categories_as_final_json_list)
        # create products
        self.create_products(products_final_json_list)
        # add relation categories with products
        self.create_relation_categories_products(products_final_json_list)
