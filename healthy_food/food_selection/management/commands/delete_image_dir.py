import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Deletes the ‘image_product’ directory and all its contents.."

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        # Build the path to the directory to be deleted in a robust manner
        dir_path = os.path.join(
            settings.BASE_DIR, 'food_selection', 'static', 'food_selection', 'images', 'image_product'
        )

        if not silent:
            self.stdout.write(f"🗑️ Tentative de suppression du répertoire : {dir_path}")

        # Check whether the directory exists before attempting to delete it.
        if os.path.exists(dir_path):
            try:
                # shutil.rmtree deletes a directory and all its contents
                shutil.rmtree(dir_path)
                if not silent:
                    self.stdout.write(self.style.SUCCESS("✅ Répertoire supprimé avec succès !"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Erreur lors de la suppression du répertoire : {e}"))
        else:
            if not silent:
                self.stdout.write(self.style.WARNING("🟡 Le répertoire n'existe pas, rien à faire."))