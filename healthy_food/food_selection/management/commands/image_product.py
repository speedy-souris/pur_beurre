
from django.core.management.base import BaseCommand
from food_selection.models import Product
import requests
import os

class Command(BaseCommand):
    help = 'add images in database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        counter = 0
        images_folder_path = "food_selection/static/food_selection/images/image_product"
        for product in products:
            counter += 1
            if counter % int((len(products) / 50)) == 0:
                print(f"compteur : {counter}/{len(products)}")
            image_product_id = product.product_id
            image_file_path = f"{images_folder_path}/{image_product_id}.jpg"
            if not os.path.exists(images_folder_path):
                os.makedirs(images_folder_path)
            if os.path.exists(image_file_path):
                continue
            try:
                response = requests.get(product.image_url)
            except requests.exceptions.MissingSchema:
                continue
            if not bool(response.content):
                continue
            else:
                if  response.status_code == 200:
                    f = open(image_file_path, "wb")
                    f.write(response.content)
                    f.close()
