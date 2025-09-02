from django.test import TestCase
from food_selection.views import get_better_nutriscore_list

class NutriscoreUtilsTest(TestCase):

    def test_get_better_nutriscore_list(self):
        # display a better Nutriscore for the selected product
        self.assertEqual(get_better_nutriscore_list('A'), ['A'])
        self.assertEqual(get_better_nutriscore_list('B'), ['A'])
        self.assertEqual(get_better_nutriscore_list('C'), ['A', 'B'])
        self.assertEqual(get_better_nutriscore_list('D'), ['A', 'B', 'C'])
        self.assertEqual(get_better_nutriscore_list('E'), ['A', 'B', 'C', 'D'])