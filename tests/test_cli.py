import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import pytest

from mackup import utils
from mackup.main import main


class TestCLI(unittest.TestCase):
    """Test suite for CLI commands: backup, restore, and copy mode workflows."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create temporary directories for testing
        self.test_home = tempfile.mkdtemp(prefix="mackup_test_home_")
        self.test_storage = tempfile.mkdtemp(prefix="mackup_test_storage_")
        self.mackup_folder = os.path.join(self.test_storage, "Mackup")

        # Store original HOME
        self.original_home = os.environ.get("HOME")
        self.original_xdg = os.environ.get("XDG_CONFIG_HOME")

        # Set HOME to our test directory
        os.environ["HOME"] = self.test_home
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.test_home, ".config")

        # Create test config file
        self.config_path = os.path.join(self.test_home, ".mackup.cfg")
        with open(self.config_path, "w") as f:
            f.write("[storage]\n")
            f.write("engine = file_system\n")
            f.write(f"path = {self.test_storage}\n")
            f.write("directory = Mackup\n")
            f.write("\n")
            f.write("[applications_to_sync]\n")
            f.write("test-app\n")

        # Create a test application config in the apps database
        self.test_app_name = "test-app"
        self.test_file_name = ".testrc"
        self.test_file_path = os.path.join(self.test_home, self.test_file_name)

        # Create test file with content
        with open(self.test_file_path, "w") as f:
            f.write("test_config=value\n")

        # Create custom application config
        self.custom_apps_dir = os.path.join(self.test_home, ".mackup")
        os.makedirs(self.custom_apps_dir, exist_ok=True)

        self.custom_app_config = os.path.join(self.custom_apps_dir, "test-app.cfg")
        with open(self.custom_app_config, "w") as f:
            f.write("[application]\n")
            f.write(f"name = {self.test_app_name}\n")
            f.write("\n")
            f.write("[configuration_files]\n")
            f.write(f"{self.test_file_name}\n")

        # Force yes to all prompts
        utils.FORCE_YES = True
        utils.FORCE_NO = False
        utils.CAN_RUN_AS_ROOT = False

    def tearDown(self):
        """Clean up test environment after each test."""
        # Restore original HOME
        if self.original_home:
            os.environ["HOME"] = self.original_home
        else:
            os.environ.pop("HOME", None)

        # Restore original XDG_CONFIG_HOME
        if self.original_xdg:
            os.environ["XDG_CONFIG_HOME"] = self.original_xdg
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)

        # Clean up temporary directories
        if os.path.exists(self.test_home):
            shutil.rmtree(self.test_home)
        if os.path.exists(self.test_storage):
            shutil.rmtree(self.test_storage)

        # Reset utils flags
        utils.FORCE_YES = False
        utils.FORCE_NO = False
        utils.CAN_RUN_AS_ROOT = False

    def test_backup_creates_mackup_folder(self):
        """Test that mackup backup creates the Mackup folder if it doesn't exist."""
        # Ensure Mackup folder doesn't exist
        assert not os.path.exists(self.mackup_folder)

        # Mock sys.argv to simulate 'mackup backup'
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Check that Mackup folder was created
        assert os.path.exists(self.mackup_folder)

    def test_backup_copies_file(self):
        """Test that mackup backup successfully copies a file to the backup location."""
        # Ensure test file exists
        assert os.path.exists(self.test_file_path)

        # Run backup
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Check that file was copied to Mackup folder
        backed_up_file = os.path.join(self.mackup_folder, self.test_file_name)
        assert os.path.exists(backed_up_file)

        # Verify content is the same
        with open(self.test_file_path) as f:
            original_content = f.read()
        with open(backed_up_file) as f:
            backed_up_content = f.read()

        assert original_content == backed_up_content

    def test_restore_copies_file_back(self):
        """Test that mackup restore successfully copies a file back from backup."""
        # First, create a backup
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Verify backup exists
        backed_up_file = os.path.join(self.mackup_folder, self.test_file_name)
        assert os.path.exists(backed_up_file)

        # Remove original file
        os.remove(self.test_file_path)
        assert not os.path.exists(self.test_file_path)

        # Run restore
        with patch("sys.argv", ["mackup", "restore"]):
            main()

        # Check that file was restored
        assert os.path.exists(self.test_file_path)

        # Verify content is correct
        with open(self.test_file_path) as f:
            restored_content = f.read()

        assert restored_content == "test_config=value\n"

    def test_backup_and_restore_full_workflow(self):
        """Test complete backup and restore workflow."""
        original_content = "test_config=value\n"

        # Verify original file exists and has correct content
        assert os.path.exists(self.test_file_path)
        with open(self.test_file_path) as f:
            assert f.read() == original_content

        # Step 1: Backup
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Verify backup was created
        backed_up_file = os.path.join(self.mackup_folder, self.test_file_name)
        assert os.path.exists(backed_up_file)

        # Step 2: Modify original file
        modified_content = "test_config=modified\n"
        with open(self.test_file_path, "w") as f:
            f.write(modified_content)

        # Verify file was modified
        with open(self.test_file_path) as f:
            assert f.read() == modified_content

        # Step 3: Restore (should replace modified file with backup)
        with patch("sys.argv", ["mackup", "restore"]):
            main()

        # Verify file was restored to original content
        with open(self.test_file_path) as f:
            assert f.read() == original_content

    def test_backup_preserves_file_permissions(self):
        """Test that mackup backup preserves file permissions."""
        # Set specific permissions on test file
        os.chmod(self.test_file_path, 0o600)

        # Run backup
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Check backup file permissions
        backed_up_file = os.path.join(self.mackup_folder, self.test_file_name)
        assert os.path.exists(backed_up_file)

        # Verify permissions are preserved (mackup sets to 0600 by default)
        backed_up_stat = os.stat(backed_up_file)
        expected_mode = 0o600
        assert backed_up_stat.st_mode & 0o777 == expected_mode

    def test_restore_with_missing_backup(self):
        """Test that mackup restore handles missing backup files gracefully."""
        # Ensure no backup exists
        assert not os.path.exists(self.mackup_folder)

        # Create the mackup folder but don't add any files
        os.makedirs(self.mackup_folder, exist_ok=True)

        # Run restore (should not crash even though no backup exists)
        with patch("sys.argv", ["mackup", "restore"]):
            try:
                main()
                # If no exception is raised, the test passes
                # (restore should gracefully handle missing files)
            except Exception as e:
                self.fail(f"Restore raised an exception with missing backup: {e}")

    def test_backup_with_folder(self):
        """Test that mackup backup works with folders, not just files."""
        # Create a test folder with a file inside
        test_folder_name = ".test_folder"
        test_folder_path = os.path.join(self.test_home, test_folder_name)
        os.makedirs(test_folder_path, exist_ok=True)

        test_file_in_folder = os.path.join(test_folder_path, "config.txt")
        with open(test_file_in_folder, "w") as f:
            f.write("folder_config=value\n")

        # Update custom app config to include the folder
        with open(self.custom_app_config, "w") as f:
            f.write("[application]\n")
            f.write(f"name = {self.test_app_name}\n")
            f.write("\n")
            f.write("[configuration_files]\n")
            f.write(f"{self.test_file_name}\n")
            f.write(f"{test_folder_name}\n")

        # Run backup
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Check that folder was copied
        backed_up_folder = os.path.join(self.mackup_folder, test_folder_name)
        assert os.path.exists(backed_up_folder)
        assert os.path.isdir(backed_up_folder)

        # Check that file inside folder was copied
        backed_up_file_in_folder = os.path.join(backed_up_folder, "config.txt")
        assert os.path.exists(backed_up_file_in_folder)

        # Verify content
        with open(backed_up_file_in_folder) as f:
            assert f.read() == "folder_config=value\n"

    def test_restore_with_folder(self):
        """Test that mackup restore works with folders."""
        # Create a test folder with a file inside
        test_folder_name = ".test_folder"
        test_folder_path = os.path.join(self.test_home, test_folder_name)
        os.makedirs(test_folder_path, exist_ok=True)

        test_file_in_folder = os.path.join(test_folder_path, "config.txt")
        with open(test_file_in_folder, "w") as f:
            f.write("folder_config=value\n")

        # Update custom app config to include the folder
        with open(self.custom_app_config, "w") as f:
            f.write("[application]\n")
            f.write(f"name = {self.test_app_name}\n")
            f.write("\n")
            f.write("[configuration_files]\n")
            f.write(f"{self.test_file_name}\n")
            f.write(f"{test_folder_name}\n")

        # Run backup first
        with patch("sys.argv", ["mackup", "backup"]):
            main()

        # Delete the folder
        shutil.rmtree(test_folder_path)
        assert not os.path.exists(test_folder_path)

        # Run restore
        with patch("sys.argv", ["mackup", "restore"]):
            main()

        # Check that folder was restored
        assert os.path.exists(test_folder_path)
        assert os.path.isdir(test_folder_path)

        # Check that file inside folder was restored
        assert os.path.exists(test_file_in_folder)

        # Verify content
        with open(test_file_in_folder) as f:
            assert f.read() == "folder_config=value\n"

    def test_restore_fails_when_mackup_folder_missing(self):
        """Test that mackup restore fails when Mackup folder doesn't exist."""
        # Ensure Mackup folder doesn't exist
        assert not os.path.exists(self.mackup_folder)

        # Run restore - should exit with error when backup folder is missing
        with patch("sys.argv", ["mackup", "restore"]):
            with pytest.raises(SystemExit) as context:
                main()

            # Should exit with non-zero status
            assert context.value.code != 0

    def test_force_and_force_no_are_mutually_exclusive(self):
        """Passing --force and --force-no together should fail fast."""
        with patch("sys.argv", ["mackup", "--force", "--force-no", "backup"]):
            with pytest.raises(SystemExit) as context:
                main()

            assert (
                str(context.value)
                == "Options --force and --force-no are mutually exclusive."
            )


if __name__ == "__main__":
    unittest.main()
