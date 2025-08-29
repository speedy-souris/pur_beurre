from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Supprime les anciennes données et importe les produits depuis OpenFoodFacts"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        if not silent:
            self.stdout.write("🧹 Suppression des anciennes données en cours ...")
        # deletes products from the database
        call_command('delete_data', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Suppressions complète des produits terminée !"))

        if not silent:
            self.stdout.write("📦 Importation des produits en cours ...")
        call_command('create_product', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Importation complète des produits terminée !"))

        if not silent:
            self.stdout.write("🖼️ Importation des images des produits en cours ...")
        call_command('image_product', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Importation complète des images terminée !"))
