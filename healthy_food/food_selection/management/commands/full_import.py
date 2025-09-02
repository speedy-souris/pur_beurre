from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Deletes old data and imports products from OpenFoodFacts"

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
        call_command('delete_all_data', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Suppressions complète des produits terminée !"))

        if not silent:
            self.stdout.write("🧹 Suppression des anciennes images en cours ...")
        # deletes images from the directory
        call_command('delete_image_dir', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Suppressions complète des images terminée !"))

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
