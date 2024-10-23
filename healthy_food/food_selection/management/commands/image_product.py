
from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import requests

class Command(BaseCommand):
    help = 'add images in database'

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            try:
                response = requests.get(product.image_url)
            except:
                continue
            if  response.status_code == 200:
                f = open("food_selection/static/food_selection/images/image_product_id.jpg", "wb")
                f.write(response.content)
                f.close()

