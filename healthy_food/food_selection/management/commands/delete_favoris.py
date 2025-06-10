from django.core.management.base import BaseCommand
from food_selection.models import Product

class Command(BaseCommand):
    help = 'delete favorite products from the database'

    def handle(self, *args, **options):
        total_products_db = Product.objects.all()
        for saved_status in total_products_db:
            saved_status.saved = False
            saved_status.save()



