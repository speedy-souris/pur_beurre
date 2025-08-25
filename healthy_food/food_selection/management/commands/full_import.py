from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Exécute create_product, image_product et image_nutrition dans l'ordre"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    def handle(self, *args, **options):
        silent = options['silent']

        # call_command('delete_data', silent=silent)
        # call_command('delete_favoris', silent=silent)
        call_command('create_product', silent=silent)
        call_command('image_product', silent=silent)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Import complet terminé."))
