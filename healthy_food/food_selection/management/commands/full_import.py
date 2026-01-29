from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Réinitialise la base Produits et importe les données OpenFoodFacts"

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux (moins de logs)'
        )

    def log(self, message, style=None, silent=False):
        if silent:
            return
        if style:
            self.stdout.write(style(message))
        else:
            self.stdout.write(message)

    def handle(self, *args, **options):
        silent = options['silent']

        steps = [
            ("🧹 Suppression des anciennes données ...",
             lambda: call_command('delete_all_data', silent=silent),
             "✅ Produits supprimés"),

            ("🧹 Suppression des anciennes images ...",
             lambda: call_command('delete_image_dir', silent=silent),
             "✅ Images supprimées"),

            ("📦 Importation des produits ...",
             lambda: call_command('create_product', silent=silent),
             "✅ Produits importés"),

            ("🖼️ Importation des images ...",
             lambda: call_command('image_product', silent=silent),
             "✅ Images importées"),
        ]

        for start_msg, action, success_msg in steps:
            self.log(start_msg, silent=silent)
            try:
                action()
                self.log(success_msg, self.style.SUCCESS, silent)
            except Exception as e:
                self.log(f"❌ Erreur : {e}", self.style.ERROR, silent)
                break
