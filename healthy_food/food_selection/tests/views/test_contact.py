from django.test import TestCase
from django.urls import reverse
from food_selection.forms import SearchNewFood, ContactUsForm


class ContactViewContextTest(TestCase):

    def test_contact_view_status_code(self):
        # status 200 on the contact page
        response = self.client.get(reverse('food_selection:contact-us'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_template_used(self):
        # contact.html template for the contact page
        response = self.client.get(reverse('food_selection:contact-us'))
        self.assertTemplateUsed(response, 'food_selection/contact.html')

    def test_contact_context_contains_expected_keys(self):
        # view context content ==> search_form & page_name & contact_form
        response = self.client.get(reverse('food_selection:contact-us'))
        self.assertIn('search_form', response.context)
        self.assertIn('contact_form', response.context)
        self.assertIn('page_name', response.context)


    def test_contact_context_page_name_value(self):
        # display the page name
        response = self.client.get(reverse('food_selection:contact-us'))
        self.assertEqual(response.context['page_name'], 'Contact')

    def test_contact_forms_are_correct_instances(self):
        # display instance send to form
        response = self.client.get(reverse('food_selection:contact-us'))
        self.assertIsInstance(response.context['search_form'], SearchNewFood)
        self.assertIsInstance(response.context['contact_form'], ContactUsForm)

