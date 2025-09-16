from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product, Category
from food_selection.forms import SearchNewFood

class FoundViewTest(TestCase):

    def setUp(self):
        # Create a categorries and product for testing
        self.category1 = Category.objects.create(name="plat_préparés")
        self.category2 = Category.objects.create(name="Boissons")
        self.Category3 = Category.objects.create(name='Desserts')
        #1. The product to be substituted (the ‘bad’ product)
        self.required_product = Product.objects.create(
            name="Plat Mauvais D",
            nutriscore="D",
            pk='1',
        )
        self.required_product.categories.add(self.category1)
        #2. A good substitute in the same category
        self.substitute_good_A = Product.objects.create(
            name="Plat Sain A",
            nutriscore="A",
            pk='2',
        )
        self.substitute_good_A.categories.add(self.category1)
        #3. Another good substitute (B) in the same category
        self.substitute_good_B = Product.objects.create(
            name="Plat Acceptable B",
            nutriscore="B",
            pk='3',
        )
        self.substitute_good_B.categories.add(self.category1)
        #4. A good quality product (A) but in a different category (SHOULD NOT BE OFFERED)
        self.irrelevant_product_A = Product.objects.create(
            name="Boisson Santé A",
            nutriscore="A",
            pk='4',
        )
        self.irrelevant_product_A.categories.add(self.category2)

    def test_found_view_status_code(self):
        # status 200 on the found page
        response = self.client.get(reverse('food_selection:found'), {'product': self.required_product.name})
        self.assertEqual(response.status_code, 200)

    def test_found_view_context(self):
        # view context content ==> search_form & page_name ...
        response = self.client.get(reverse('food_selection:found'), {'product': 'Plat Mauvais D'})
        self.assertTrue(response.context['product_found'])
        self.assertEqual(response.context['required_product'], self.required_product)
        self.assertIn('search_form', response.context)
        self.assertEqual(response.context['name'], 'Plat Mauvais D')

    def test_found_view_alternative_products(self):
        # view alternative_product
        response = self.client.get(reverse('food_selection:found'), {'product': 'Plat Mauvais D'})
        alternative_products = response.context['products']
        # Check that alternative products have better Nutriscores than D.
        self.assertTrue(all(p.nutriscore in ['A', 'B', 'C'] for p in alternative_products))

    def test_found_view_with_multiple_categories(self):
        # Add a second category to the product for this specific test
        self.required_product.categories.add(self.category2)
        # Make a request to the found view
        response = self.client.get(reverse('food_selection:found'), {'product': 'Plat Mauvais D'})
        # Check that the response is successful
        self.assertEqual(response.status_code, 200)
        # Get the product from the context
        product_in_context = response.context['required_product']
        # Check that the product in the context has the correct number of categories
        self.assertEqual(product_in_context.categories.count(), 2)
        # Check that the product's categories are the ones we assigned
        categories_in_context = list(product_in_context.categories.all())
        self.assertIn(self.category1, categories_in_context)
        self.assertIn(self.category2, categories_in_context)

    def test_found_view_substitution_logic(self):
        """
            Tests whether the view returns only substitute
            products that share a category AND have a better Nutri - Score.
        """
        # The product to search for is self.required_product
        response = self.client.get(
            reverse('food_selection:found'),
            {'product': self.required_product.name}
        )
        self.assertEqual(response.status_code, 200)
        alternative_products = response.context['products']
        #1. Check the number of substitutions: there should be 2.
        self.assertEqual(len(alternative_products), 2)
        #2. Verify that the substitutes are indeed the relevant products.
        substitute_names = [p.name for p in alternative_products]
        self.assertIn("Plat Sain A", substitute_names)
        self.assertIn("Plat Acceptable B", substitute_names)
        #3. Verify that the irrelevant product is NOT included.
        self.assertNotIn("Boisson Santé A", substitute_names)
        #4. Check the Nutri-Score quality (A or B)
        self.assertTrue(all(p.nutriscore in ['A', 'B', 'C'] for p in alternative_products))
        #5. Verify that the original product is not on the substitution list.
        self.assertNotIn(self.required_product, alternative_products)
