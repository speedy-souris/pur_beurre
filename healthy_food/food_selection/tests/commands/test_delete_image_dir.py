import os
import shutil  # Importing shutil is a good practice for cleanup.
import tempfile
from django.core.management import call_command
from django.test import TestCase, override_settings

TEMP_PROJECT_ROOT = tempfile.TemporaryDirectory()

@override_settings(BASE_DIR=TEMP_PROJECT_ROOT.name)
class DeleteImageDirCommandTest(TestCase):

    # TEARDOWN METHOD
    def tearDown(self):
        """
        Cleans the contents of the temporary directory after each test.
        """
        # We go through everything in the temporary directory.
        for item in os.listdir(TEMP_PROJECT_ROOT.name):
            item_path = os.path.join(TEMP_PROJECT_ROOT.name, item)
            # If it is a folder, delete it recursively.
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            # If it is a file, delete it.
            else:
                os.remove(item_path)

    def test_command_deletes_existing_directory(self):
        """
        Test that the command deletes the directory if it exists.
        """
        # --- 1. SETUP ---
        dir_to_delete = os.path.join(
            TEMP_PROJECT_ROOT.name, 'food_selection', 'static', 'food_selection', 'images', 'image_product'
        )
        os.makedirs(dir_to_delete)
        with open(os.path.join(dir_to_delete, 'test_image.jpg'), 'w') as f:
            f.write('fake image data')

        # --- 2. PRE-ASSERTION ---
        self.assertTrue(os.path.exists(dir_to_delete))

        # --- 3. EXECUTION ---
        # Ensure that your command file is named delete_image_dir.py.
        call_command('delete_image_dir', '--silent')

        # --- 4. POST-ASSERTION ---
        self.assertFalse(os.path.exists(dir_to_delete))

    def test_command_handles_non_existing_directory(self):
        """
        Tests that the command does not raise an error if the directory does not exist.
        """
        # --- 1. SETUP ---
        dir_that_does_not_exist = os.path.join(
            TEMP_PROJECT_ROOT.name, 'food_selection', 'static', 'food_selection', 'images', 'image_product'
        )

        # --- 2. PRE-ASSERTION ---
        self.assertFalse(os.path.exists(dir_that_does_not_exist))

        # --- 3. EXECUTION & ASSERTION ---
        try:
            # Ensure that your command file is named delete_image_dir.py.
            call_command('delete_image_dir', '--silent')
        except Exception as e:
            self.fail(f"La commande a levé une exception inattendue : {e}")

        self.assertFalse(os.path.exists(dir_that_does_not_exist))