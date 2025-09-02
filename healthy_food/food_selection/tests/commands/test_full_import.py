from unittest.mock import patch, call
from django.core.management import call_command
from django.test import TestCase

class UpdateAllCommandTest(TestCase):

    # We mock ‘call_command’ IN the module where it is used,
    # that is, in your order file.
    @patch('food_selection.management.commands.full_import.call_command')
    def test_handle_calls_subcommands_in_correct_order(self, mock_call_command):
        """
        Tests that the main command calls the subcommands
        in the correct order and with the correct arguments.
        """
        # --- EXECUTION ---
        # The main command to be tested is executed.
        call_command('full_import', '--silent')

        # --- ASSERTIONS ---
        # We verify that our mock has been called three times.
        self.assertEqual(mock_call_command.call_count, 4)

        # We prepare a list of calls that we expect to receive.
        # The `call` object from unittest.mock makes this verification very readable.
        expected_calls = [
            call('delete_all_data', silent=True),
            call('delete_image_dir', silent=True),
            call('create_product', silent=True),
            call('image_product', silent=True)
        ]

        # We verify that the list of calls made on the mock
        # matches our expected list exactly (including the order).
        mock_call_command.assert_has_calls(expected_calls, any_order=False)
