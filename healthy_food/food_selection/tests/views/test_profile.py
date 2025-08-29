from django.test import TestCase
from django.urls import reverse
from food_selection.forms import SearchNewFood

class ProfileViewTest(TestCase):

    def test_profile_view_status_code(self):
        # status 200 on the profile page
        response = self.client.get(reverse('food_selection:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_template_used(self):
        # profile.html template for the profile page
        response = self.client.get(reverse('food_selection:profile'))
        self.assertTemplateUsed(response, 'food_selection/profile.html')

    def test_profile_context_contains_expected_keys(self):
        # view context content ==> search_form & page_name
        response = self.client.get(reverse('food_selection:profile'))
        self.assertIn('search_form', response.context)
        self.assertIn('page_name', response.context)

    def test_profile_context_page_name_value(self):
        # display the page name
        response = self.client.get(reverse('food_selection:profile'))
        self.assertEqual(response.context['page_name'], 'Profile')

    def test_profile_search_form_instance(self):
        # display instance send to form
        response = self.client.get(reverse('food_selection:profile'))
        self.assertIsInstance(response.context['search_form'], SearchNewFood)
