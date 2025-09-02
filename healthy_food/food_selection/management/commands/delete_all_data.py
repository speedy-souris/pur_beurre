from django.core.management.base import BaseCommand
from food_selection.models import Product, Category

class Command(BaseCommand):
    help = "Deletes all data from the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    def handle(self, *args, **options):
        silent = options['silent']
        all_products_db = Product.objects.all()
        all_categories_db = Category.objects.all()

        if not silent:
            self.stdout.write("🚀 Suppression des produits et catégories...")

        all_products_db.delete()
        all_categories_db.delete()

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Suppression terminée"))
