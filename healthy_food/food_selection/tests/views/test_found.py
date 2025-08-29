from django.test import TestCase
from django.urls import reverse
from food_selection.models import Product, Category
from food_selection.forms import SearchNewFood

class FoundViewTest(TestCase):

    def setUp(self):
        # Create a category and product for testing
        self.category = Category.objects.create(name="TestCategory")
        self.product = Product.objects.create(
            name="TestProduct",
            nutriscore="D",
            pk='1',
        )
        self.product.categories.add(self.category)

    def test_found_view_status_code(self):
        # status 200 on the found page
        response = self.client.get(reverse('food_selection:found'), {'product': self.product.name})
        self.assertEqual(response.status_code, 200)

    def test_found_view_context(self):
        # view context content ==> search_form & page_name ...
        response = self.client.get(reverse('food_selection:found'), {'product': 'TestProduct'})
        self.assertTrue(response.context['product_found'])
        self.assertEqual(response.context['required_product'], self.product)
        self.assertIn('search_form', response.context)
        self.assertEqual(response.context['name'], 'TestProduct')

    def test_found_view_alternative_products(self):
        # view alternative_product
        response = self.client.get(reverse('food_selection:found'), {'product': 'TestProduct'})
        alternative_products = response.context['products']
        # Check that alternative products have better Nutriscores than D.
        self.assertTrue(all(p.nutriscore in ['A', 'B', 'C'] for p in alternative_products))
