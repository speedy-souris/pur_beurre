from django.core.management.base import BaseCommand
from food_selection.models import Product, Category
import requests

class Command(BaseCommand):
    help = 'Importe les produits et catégories depuis OpenFoodFacts dans la base de données'

    # Catégories au format API (remplace espaces/accents par tirets)
    CATEGORIES_TO_FETCH = [
        'pates-alimentaires-de-cereales', 'boissons', 'melanges-de-legumes-frais',
        'fruits-secs', 'poissons', 'biscottes', 'patisseries', 'fromages',
        'charcuteries', 'confitures'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            help='Mode silencieux, supprime les logs détaillés'
        )

    @staticmethod
    def create_categories(categories_list):
        existing_categories = set(Category.objects.filter(name__in=categories_list).values_list('name', flat=True))
        new_categories = [Category(name=cat) for cat in set(categories_list) if cat not in existing_categories]
        Category.objects.bulk_create(new_categories)

    @staticmethod
    def create_products(products_list):
        existing_product_ids = set(
            Product.objects.filter(product_id__in=[p['product_id'] for p in products_list]).values_list('product_id', flat=True)
        )
        new_products = []
        for prod in products_list:
            if len(prod['nutriscore']) != 1:
                continue
            if prod['product_id'] in existing_product_ids:
                continue
            new_products.append(Product(
                name=prod['name'],
                product_id=prod['product_id'],
                nutriscore=prod['nutriscore'],
                nutriments=prod['nutriments'],
                url=prod['url'],
                image_url=prod['image_url'],
            ))
            # print(f'nutriments = {prod["nutriments"]}')
        Product.objects.bulk_create(new_products)

    @staticmethod
    def create_relations(products_list):
        for prod in products_list:
            try:
                product_obj = Product.objects.get(product_id=prod['product_id'])
            except Product.DoesNotExist:
                continue
            for category_name in prod['categories']:
                try:
                    category_obj = Category.objects.get(name=category_name)
                    product_obj.categories.add(category_obj)
                except Category.DoesNotExist:
                    pass

    def handle(self, *args, **options):
        silent = options['silent']

        if not silent:
            self.stdout.write("🚀 Démarrage de l'importation des produits...")

        products_final = []
        total_count = 0

        for category_name in self.CATEGORIES_TO_FETCH:
            url = (
                f"https://fr.openfoodfacts.org/api/v1/search?categories_tags_fr={category_name}"
                 "&fields=code,product_name_fr,nutriscore_grade,categories_tags_fr,url,image_url,nutriments"
                 "&page=1&page_size=100"
            )

            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                if not silent:
                    self.stderr.write(f"❌ Erreur API pour la catégorie '{category_name}': {e}")
                continue

            products = data.get('products', [])

            if not silent:
                self.stdout.write(f"📦 {len(products)} produits trouvés dans la catégorie '{category_name}'")

            for item in products:
                if not item.get('product_name_fr'):
                    continue

                nutriscore = item.get('nutriscore_grade', '').upper()
                if len(nutriscore) != 1 or nutriscore not in ['A', 'B', 'C', 'D', 'E']:
                    continue

                nutriments = item.get('nutriments')
                keys_to_keep = {
                    "sugars_100g", "salt_100g",
                    "energy_100g", "proteins_100g",
                    "carbohydrates_100g", "fiber_100g",
                    "fat_100g", "satured_fat_100g"
                }
                nutriments = {key: value for key, value in nutriments.items() if key in keys_to_keep}
                # print(f' nutriments = {nutriments}')
                def valid_url(url):
                    return isinstance(url, str) and url.startswith('http')

                image_url = item.get('image_url') if valid_url(item.get('image_url')) else None

                categories_filtered = [
                    c.lower() for c in item.get('categories_tags_fr', [])
                    if c.lower() in self.CATEGORIES_TO_FETCH
                ]

                products_final.append({
                    'name': item['product_name_fr'],
                    'product_id': item['code'],
                    'nutriscore': nutriscore,
                    'nutriments': nutriments,
                    'url': item.get('url', ''),
                    'image_url': image_url,
                    'categories': categories_filtered,
                })

                total_count += 1
                if not silent and total_count % 50 == 0:
                    self.stdout.write(f"➡️ {total_count} produits récupérés...")

        all_categories = set(cat for prod in products_final for cat in prod['categories'])

        if not silent:
            self.stdout.write(f"📁 Création de {len(all_categories)} catégories uniques...")
        self.create_categories(list(all_categories))

        if not silent:
            self.stdout.write(f"🛒 Création de {len(products_final)} produits...")
        self.create_products(products_final)

        if not silent:
            self.stdout.write(f"🔗 Création des relations catégories-produits...")
        self.create_relations(products_final)

        if not silent:
            self.stdout.write(self.style.SUCCESS("✅ Importation des produits terminée avec succès !"))
