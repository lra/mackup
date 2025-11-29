"""Test the edge case: running backup after link install."""
import os
import tempfile
import unittest
from unittest.mock import Mock
from io import StringIO
import shutil
import sys

from mackup.application import ApplicationProfile
from mackup.mackup import Mackup


class TestBackupAfterLinkInstall(unittest.TestCase):
    """Integration test for backup after link install edge case."""

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

    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original HOME
        if self.original_home:
            os.environ["HOME"] = self.original_home
        else:
            del os.environ["HOME"]

        # Clean up temporary directories
        if os.path.exists(self.temp_home):
            shutil.rmtree(self.temp_home)
        if os.path.exists(self.mock_mackup.mackup_folder):
            shutil.rmtree(self.mock_mackup.mackup_folder)

    def test_backup_after_link_install_does_not_delete_mackup_files(self):
        """
        Test the complete scenario:
        1. Run link install (moves files to mackup and creates symlinks)
        2. Run backup (should skip already linked files)
        This prevents mackup from trying to delete files in the backup folder.
        """
        # Define test files for this test
        test_files = {".testfile", ".testdir"}

        # Step 1: Simulate initial state - files exist in home
        test_file = ".testfile"
        test_dir = ".testdir"
        home_file = os.path.join(self.temp_home, test_file)
        home_dir = os.path.join(self.temp_home, test_dir)
        
        # Create initial files
        with open(home_file, "w") as f:
            f.write("original file content")
        os.makedirs(home_dir)
        with open(os.path.join(home_dir, "subfile.txt"), "w") as f:
            f.write("original dir content")

        # Step 2: Run link install
        app_profile = ApplicationProfile(
            mackup=self.mock_mackup,
            files=test_files,
            dry_run=False,
            verbose=False
        )
        
        captured_output = StringIO()
        sys.stdout = captured_output
        app_profile.link_install()
        sys.stdout = sys.__stdout__
        
        # Verify link install worked correctly
        mackup_file = os.path.join(self.mock_mackup.mackup_folder, test_file)
        mackup_dir = os.path.join(self.mock_mackup.mackup_folder, test_dir)
        
        # Files should exist in mackup folder
        self.assertTrue(os.path.exists(mackup_file))
        self.assertTrue(os.path.exists(mackup_dir))
        
        # Home should have symlinks pointing to mackup
        self.assertTrue(os.path.islink(home_file))
        self.assertTrue(os.path.islink(home_dir))
        self.assertTrue(os.path.samefile(home_file, mackup_file))
        self.assertTrue(os.path.samefile(home_dir, mackup_dir))
        
        # Verify content is preserved
        with open(mackup_file, "r") as f:
            self.assertEqual(f.read(), "original file content")
        with open(os.path.join(mackup_dir, "subfile.txt"), "r") as f:
            self.assertEqual(f.read(), "original dir content")

        # Step 3: Run backup (this is where the edge case would occur)
        captured_output = StringIO()
        sys.stdout = captured_output
        app_profile.copy_files_to_mackup_folder()
        output = captured_output.getvalue()
        sys.stdout = sys.__stdout__
        
        # Verify backup skipped the already linked files
        # Should not print "Backing up" for these files
        self.assertNotIn("Backing up", output)
        
        # Verify the mackup files still exist and weren't deleted
        self.assertTrue(os.path.exists(mackup_file))
        self.assertTrue(os.path.exists(mackup_dir))
        
        # Verify content is still intact
        with open(mackup_file, "r") as f:
            self.assertEqual(f.read(), "original file content")
        with open(os.path.join(mackup_dir, "subfile.txt"), "r") as f:
            self.assertEqual(f.read(), "original dir content")
        
        # Verify symlinks are still in place
        self.assertTrue(os.path.islink(home_file))
        self.assertTrue(os.path.islink(home_dir))
        self.assertTrue(os.path.samefile(home_file, mackup_file))
        self.assertTrue(os.path.samefile(home_dir, mackup_dir))

    def test_backup_after_link_install_verbose_shows_skip_message(self):
        """Test that verbose mode shows skip messages for already linked files."""
        # Define test file for this test
        test_files = {".testfile"}

        # Create initial file
        test_file = ".testfile"
        home_file = os.path.join(self.temp_home, test_file)
        
        with open(home_file, "w") as f:
            f.write("test content")

        # Run link install
        app_profile = ApplicationProfile(
            mackup=self.mock_mackup,
            files=test_files,
            dry_run=False,
            verbose=False
        )
        app_profile.link_install()
        
        # Run backup in verbose mode
        app_profile_verbose = ApplicationProfile(
            mackup=self.mock_mackup,
            files=test_files,
            dry_run=False,
            verbose=True
        )
        
        captured_output = StringIO()
        sys.stdout = captured_output
        app_profile_verbose.copy_files_to_mackup_folder()
        output = captured_output.getvalue()
        sys.stdout = sys.__stdout__
        
        # Verify skip message is shown
        self.assertIn("Skipping", output)
        self.assertIn("already linked to", output)
        self.assertIn(home_file, output)


if __name__ == "__main__":
    unittest.main()
