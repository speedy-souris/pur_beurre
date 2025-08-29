from django.test import TestCase
from django.urls import reverse
from food_selection.forms import SearchNewFood

class DisclaimerViewTest(TestCase):

    def test_disclaimer_view_status_code(self):
        # status 200 on the disclaimer page
        response = self.client.get(reverse('food_selection:disclaimer'))
        self.assertEqual(response.status_code, 200)

    def test_disclaimer_view_template_used(self):
        # legal_disclaimer.html template for the disclaimer page
        response = self.client.get(reverse('food_selection:disclaimer'))
        self.assertTemplateUsed(response, 'food_selection/legal_disclaimer.html')

    def test_disclaimer_context_contains_expected_keys(self):
        # view context content ==> search_form & page_name
        response = self.client.get(reverse('food_selection:disclaimer'))
        self.assertIn('search_form', response.context)
        self.assertIn('page_name', response.context)

    def test_disclaimer_context_page_name_value(self):
        # display the page name
        response = self.client.get(reverse('food_selection:disclaimer'))
        self.assertEqual(response.context['page_name'], 'Mentions légales')

    def test_disclaimer_search_form_instance(self):
        # display instance send to form
        response = self.client.get(reverse('food_selection:disclaimer'))
        self.assertIsInstance(response.context['search_form'], SearchNewFood)
