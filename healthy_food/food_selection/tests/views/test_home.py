from django.test import TestCase
from django.urls import reverse
from food_selection.forms import SearchNewFood

class HomeViewTest(TestCase):

    def test_home_view_status_code(self):
        # status 200 on the home page
        response = self.client.get(reverse('food_selection:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        # home.html template for the home page
        response = self.client.get(reverse('food_selection:home'))
        self.assertTemplateUsed(response, 'food_selection/home.html')

    def test_home_context_contains_expected_keys(self):
        # view context content ==> search_form & page_name
        response = self.client.get(reverse('food_selection:home'))
        self.assertIn('search_form', response.context)
        self.assertIn('page_name', response.context)

    def test_home_context_page_name_value(self):
        # display the page name
        response = self.client.get(reverse('food_selection:home'))
        self.assertEqual(response.context['page_name'], 'Accueil')

    def test_home_search_form_instance(self):
        # display instance send to form
        response = self.client.get(reverse('food_selection:home'))
        self.assertIsInstance(response.context['search_form'], SearchNewFood)


