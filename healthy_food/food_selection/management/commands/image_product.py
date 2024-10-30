
from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import requests

class Command(BaseCommand):
    help = 'add images in database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        counter = 0
        for product in products:
            image_product_id = product.product_id
            try:
                response = requests.get(product.image_url)
            except Exception as inst:
                print(type(inst))
                continue
            if  response.status_code == 200:
                f = open(f"food_selection/static/food_selection/images/{image_product_id}.jpg", "wb")
                f.write(response.content)
                f.close()
            counter += 1
            if counter % int((len(products)/50)) == 0 :
              print(f"compteur : {counter}/{len(products)}")

