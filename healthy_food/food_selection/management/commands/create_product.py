from django.core.management.base import BaseCommand
from django.conf import settings
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
                                         url=product_as_json['url'],
                                         image_url=product_as_json['image_url'],
                                         image_nutrition_url=product_as_json['image_nutrition_url']
                                         ))
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
                    # print(f'produit = {product_as_json}')
                    product_as_object.categories.add(category_as_object)

    def handle(self, *args, **options):
        products_final_json_list = []
        categories_object_list = ['pâtes alimentaires de céréales', 'boissons',
                                  'mélanges de légumes frais', 'fruits secs', 'poissons',
                                  'biscottes', 'pâtisseries', 'fromages', 'charcuteries', 'confitures']
        counter = 1
        for category_as_element in categories_object_list:
            url = f"https://fr.openfoodfacts.org/api/v1/search?categories_tags_fr={category_as_element}" \
                  "&fields=code,product_name_fr,nutriscore_grade,categories_tags_fr,url,image_url,image_nutrition_url&page=1&page_size=100"

            product_infos = requests.get(url)
            data_as_json = json.loads(product_infos.text)
            for product_as_object in data_as_json['products']:
                # Filtrage produit minimal
                if 'product_name_fr' not in product_as_object or not product_as_object['product_name_fr']:
                    continue
                if 'nutriscore_grade' not in product_as_object or len(product_as_object['nutriscore_grade']) != 1:
                    continue

                # Validation des URLs d'images
                def valid_url(url):
                    return isinstance(url, str) and url.startswith('http')

                image_url = product_as_object.get('image_url')
                image_nutrition_url = product_as_object.get('image_nutrition_url')

                if not valid_url(image_url):
                    image_url = None
                if not valid_url(image_nutrition_url):
                    image_nutrition_url = None

                # Filtrer uniquement ceux avec nutriscore correct
                nutriscore = product_as_object['nutriscore_grade'].upper()
                if nutriscore not in ['A', 'B', 'C', 'D', 'E']:
                    continue

                name_object = product_as_object['product_name_fr']
                categories_limited = [c.lower() for c in product_as_object.get('categories_tags_fr', [])
                                      if c.lower() in categories_object_list]

                create_final_product_object = {
                    'name': name_object,
                    'categories': categories_limited,
                    'nutriscore': nutriscore,
                    'url': product_as_object.get('url', ''),
                    'product_id': product_as_object['code'],
                    'image_url': image_url,
                    'image_nutrition_url': image_nutrition_url,
                }
                products_final_json_list.append(create_final_product_object)
                counter += 1

        categories_as_final_json_list = [cat for prod in products_final_json_list for cat in prod['categories']]

        self.create_categories(categories_as_final_json_list)
        self.create_products(products_final_json_list)
        self.create_relation_categories_products(products_final_json_list)
