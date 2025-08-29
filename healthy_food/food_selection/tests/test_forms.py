from django.test import TestCase
from food_selection.forms import SearchNewFood, ContactUsForm, SaveProductForm

class SearchNewFoodFormTest(TestCase):
    def test_valid_form(self):
        # Form valid if ‘product’ is provided
        form_data = {'product': 'Chocolat'}
        form = SearchNewFood(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['product'], 'Chocolat')

    def test_invalid_form_when_empty(self):
        # Form invalid if ‘product’ is empty
        form = SearchNewFood(data={'product': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('product', form.errors)

    def test_field_label(self):
        # The label for the ‘product’ field must be correct
        form = SearchNewFood()
        self.assertEqual(form.fields['product'].label, 'produit recherché')


class ContactUsFormTest(TestCase):
    def test_valid_form(self):
        # Valid form with correct data
        form_data = {
            'first_name': 'Pascal',
            'email': 'pascal@example.com',
            'message': 'Bonjour, ceci est un test.'
        }
        form = ContactUsForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'Pascal')

    def test_invalid_without_first_name(self):
        # Invalid if first name is missing
        form_data = {
            'first_name': '',
            'email': 'pascal@example.com',
            'message': 'Message test'
        }
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_invalid_email_format(self):
        # Invalid if the email is not valid
        form_data = {
            'first_name': 'Pascal',
            'email': 'pascal@invalid',
            'message': 'Message test'
        }
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_message_too_long(self):
        # Invalid if message > 1000 characters
        long_message = 'a' * 1001
        form_data = {
            'first_name': 'Pascal',
            'email': 'pascal@example.com',
            'message': long_message
        }
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)


class SaveProductFormTest(TestCase):
    def test_valid_form(self):
        # Form valid when product_id is provided
        form_data = {'product_id': '123456'}
        form = SaveProductForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['product_id'], '123456')

    def test_invalid_when_missing_product_id(self):
        # Form invalid if product_id is missing
        form_data = {}
        form = SaveProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('product_id', form.errors)

    def test_invalid_when_product_id_empty(self):
        # Form invalid if product_id is empty
        form_data = {'product_id': ''}
        form = SaveProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('product_id', form.errors)


