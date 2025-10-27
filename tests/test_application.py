import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from io import StringIO
import sys

from mackup.application import ApplicationProfile
from mackup.mackup import Mackup


class TestApplicationProfile(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock Mackup instance
        self.mock_mackup = Mock(spec=Mackup)
        self.mock_mackup.mackup_folder = tempfile.mkdtemp()

        # Create a temporary home directory
        self.temp_home = tempfile.mkdtemp()

        # Save original HOME and set it to temp directory
        self.original_home = os.environ.get("HOME")
        os.environ["HOME"] = self.temp_home

        # Define test files
        self.test_files = {".testfile", ".testfolder"}

        # Create the ApplicationProfile instance
        self.app_profile = ApplicationProfile(
            mackup=self.mock_mackup,
            files=self.test_files,
            dry_run=False,
            verbose=False
        )

    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original HOME
        if self.original_home:
            os.environ["HOME"] = self.original_home
        else:
            del os.environ["HOME"]

        # Clean up temporary directories
        import shutil
        if os.path.exists(self.temp_home):
            shutil.rmtree(self.temp_home)
        if os.path.exists(self.mock_mackup.mackup_folder):
            shutil.rmtree(self.mock_mackup.mackup_folder)

    def test_copy_files_to_mackup_folder_permission_error(self):
        """Test that PermissionError is caught and handled in copy_files_to_mackup_folder."""
        # Create a test file in the home directory
        test_file = ".testfile"
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create the actual file
        with open(home_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.copy_files_to_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the error message was printed
            output = captured_output.getvalue()
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)
            self.assertIn(home_filepath, output)

    def test_copy_files_to_mackup_folder_permission_error_verbose(self):
        """Test PermissionError handling in copy_files_to_mackup_folder with verbose mode."""
        # Create a verbose ApplicationProfile
        app_profile_verbose = ApplicationProfile(
            mackup=self.mock_mackup,
            files=self.test_files,
            dry_run=False,
            verbose=True
        )

        # Create a test file in the home directory
        test_file = ".testfile"
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create the actual file
        with open(home_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            app_profile_verbose.copy_files_to_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the verbose backing up message and error message were printed
            output = captured_output.getvalue()
            self.assertIn("Backing up", output)
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)

    def test_copy_files_from_mackup_folder_permission_error(self):
        """Test that PermissionError is caught and handled in copy_files_from_mackup_folder."""
        # Create a test file in the mackup directory
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)

        # Create the actual file
        with open(mackup_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.copy_files_from_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the error message was printed
            output = captured_output.getvalue()
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)
            self.assertIn(mackup_filepath, output)

    def test_copy_files_from_mackup_folder_permission_error_verbose(self):
        """Test PermissionError handling in copy_files_from_mackup_folder with verbose mode."""
        # Create a verbose ApplicationProfile
        app_profile_verbose = ApplicationProfile(
            mackup=self.mock_mackup,
            files=self.test_files,
            dry_run=False,
            verbose=True
        )

        # Create a test file in the mackup directory
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)

        # Create the actual file
        with open(mackup_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            app_profile_verbose.copy_files_from_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the verbose recovering message and error message were printed
            output = captured_output.getvalue()
            self.assertIn("Recovering", output)
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)

    def test_copy_files_to_mackup_folder_with_directory_permission_error(self):
        """Test PermissionError with a directory in copy_files_to_mackup_folder."""
        # Create a test directory in the home directory
        test_dir = ".testfolder"
        home_dirpath = os.path.join(self.temp_home, test_dir)
        os.makedirs(home_dirpath)

        # Create a file inside the directory
        with open(os.path.join(home_dirpath, "testfile.txt"), "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied for directory")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.copy_files_to_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the error message was printed
            output = captured_output.getvalue()
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)
            self.assertIn(home_dirpath, output)

    def test_copy_files_from_mackup_folder_with_directory_permission_error(self):
        """Test PermissionError with a directory in copy_files_from_mackup_folder."""
        # Create a test directory in the mackup directory
        test_dir = ".testfolder"
        mackup_dirpath = os.path.join(self.mock_mackup.mackup_folder, test_dir)
        os.makedirs(mackup_dirpath)

        # Create a file inside the directory
        with open(os.path.join(mackup_dirpath, "testfile.txt"), "w") as f:
            f.write("test content")

        # Patch utils.copy to raise PermissionError
        with patch("mackup.application.utils.copy") as mock_copy:
            mock_copy.side_effect = PermissionError("Permission denied for directory")

            # Capture stdout to verify the error message
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.copy_files_from_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was called
            mock_copy.assert_called_once()

            # Verify that the error message was printed
            output = captured_output.getvalue()
            self.assertIn("Error: Unable to copy file", output)
            self.assertIn("permission issue", output)
            self.assertIn(mackup_dirpath, output)

    def test_copy_files_to_mackup_folder_dry_run_no_permission_error(self):
        """Test that dry_run mode doesn't trigger PermissionError in copy_files_to_mackup_folder."""
        # Create a dry_run ApplicationProfile
        app_profile_dry = ApplicationProfile(
            mackup=self.mock_mackup,
            files=self.test_files,
            dry_run=True,
            verbose=False
        )

        # Create a test file in the home directory
        test_file = ".testfile"
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create the actual file
        with open(home_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy - it should NOT be called in dry_run mode
        with patch("mackup.application.utils.copy") as mock_copy:
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            app_profile_dry.copy_files_to_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was NOT called (dry_run mode)
            mock_copy.assert_not_called()

            # Verify that the backing up message was printed
            output = captured_output.getvalue()
            self.assertIn("Backing up", output)

    def test_copy_files_from_mackup_folder_dry_run_no_permission_error(self):
        """Test that dry_run mode doesn't trigger PermissionError in copy_files_from_mackup_folder."""
        # Create a dry_run ApplicationProfile
        app_profile_dry = ApplicationProfile(
            mackup=self.mock_mackup,
            files=self.test_files,
            dry_run=True,
            verbose=False
        )

        # Create a test file in the mackup directory
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)

        # Create the actual file
        with open(mackup_filepath, "w") as f:
            f.write("test content")

        # Patch utils.copy - it should NOT be called in dry_run mode
        with patch("mackup.application.utils.copy") as mock_copy:
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            app_profile_dry.copy_files_from_mackup_folder()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that copy was NOT called (dry_run mode)
            mock_copy.assert_not_called()

            # Verify that the recovering message was printed
            output = captured_output.getvalue()
            self.assertIn("Recovering", output)

    def test_link_uninstall_mackup_not_a_link(self):
        """Test that link_uninstall skips and warns when mackup file is not a symbolic link."""
        # Create a test file in the mackup directory (regular file, not a link)
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create the mackup file as a regular file (not a link)
        with open(mackup_filepath, "w") as f:
            f.write("mackup content")

        # Create the home file
        with open(home_filepath, "w") as f:
            f.write("home content")

        # Patch utils.delete and utils.copy
        with patch("mackup.application.utils.delete") as mock_delete, \
             patch("mackup.application.utils.copy") as mock_copy:
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.link_uninstall()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that delete and copy were NOT called
            mock_delete.assert_not_called()
            mock_copy.assert_not_called()

            # Verify that the warning message was printed
            output = captured_output.getvalue()
            self.assertIn("Warning: the file in Mackup", output)
            self.assertIn("does not point to the original file", output)
            self.assertIn(mackup_filepath, output)
            self.assertIn(home_filepath, output)
            self.assertIn("skipping", output)

    def test_link_uninstall_mackup_points_to_wrong_target(self):
        """Test that link_uninstall skips and warns when mackup link points to wrong target."""
        # Create a test file
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create a different target file
        wrong_target = os.path.join(self.temp_home, ".wrongtarget")
        with open(wrong_target, "w") as f:
            f.write("wrong target content")

        # Create the mackup file as a symbolic link pointing to the wrong target
        os.symlink(wrong_target, mackup_filepath)

        # Create the home file
        with open(home_filepath, "w") as f:
            f.write("home content")

        # Patch utils.delete and utils.copy
        with patch("mackup.application.utils.delete") as mock_delete, \
             patch("mackup.application.utils.copy") as mock_copy:
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.link_uninstall()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that delete and copy were NOT called
            mock_delete.assert_not_called()
            mock_copy.assert_not_called()

            # Verify that the warning message was printed
            output = captured_output.getvalue()
            self.assertIn("Warning: the file in Mackup", output)
            self.assertIn("does not point to the original file", output)
            self.assertIn(mackup_filepath, output)
            self.assertIn(home_filepath, output)
            self.assertIn("skipping", output)

    def test_link_uninstall_mackup_points_correctly(self):
        """Test that link_uninstall proceeds normally when mackup link points to home file correctly."""
        # Create a test file
        test_file = ".testfile"
        mackup_filepath = os.path.join(self.mock_mackup.mackup_folder, test_file)
        home_filepath = os.path.join(self.temp_home, test_file)

        # Create the home file first
        with open(home_filepath, "w") as f:
            f.write("home content")

        # Create the mackup file as a symbolic link pointing to the home file
        os.symlink(home_filepath, mackup_filepath)

        # Patch utils.delete and utils.copy
        with patch("mackup.application.utils.delete") as mock_delete, \
             patch("mackup.application.utils.copy") as mock_copy:
            # Capture stdout
            captured_output = StringIO()
            sys.stdout = captured_output

            # Call the method
            self.app_profile.link_uninstall()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Verify that delete and copy WERE called (normal operation)
            mock_delete.assert_called_once_with(home_filepath)
            mock_copy.assert_called_once_with(mackup_filepath, home_filepath)

            # Verify that the reverting message was printed (not warning)
            output = captured_output.getvalue()
            self.assertIn("Reverting", output)
            self.assertNotIn("Warning", output)


if __name__ == "__main__":
    unittest.main()
