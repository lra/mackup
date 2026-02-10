"""Tests for ApplicationsDatabase XDG support."""

import os
import unittest

from mackup.appsdb import ApplicationsDatabase


class TestApplicationsDatabaseXDG(unittest.TestCase):
    """Test XDG Base Directory support for custom applications."""

    def setUp(self):
        """Set up test fixtures."""
        realpath = os.path.dirname(os.path.realpath(__file__))
        self.fixtures_path = os.path.join(realpath, "fixtures")
        os.environ["HOME"] = self.fixtures_path

        # Clear XDG_CONFIG_HOME to ensure clean state
        os.environ.pop("XDG_CONFIG_HOME", None)

    def test_legacy_custom_apps_dir(self):
        """Test that legacy ~/.mackup/ directory is found."""
        # Don't set XDG_CONFIG_HOME, only legacy should be found
        config_files = ApplicationsDatabase.get_config_files()
        filenames = {os.path.basename(f) for f in config_files}

        self.assertIn("legacy-test-app.cfg", filenames)

    def test_xdg_custom_apps_dir(self):
        """Test that XDG custom apps directory is found."""
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.fixtures_path, "xdg-config-home")

        config_files = ApplicationsDatabase.get_config_files()
        filenames = {os.path.basename(f) for f in config_files}

        self.assertIn("xdg-test-app.cfg", filenames)

    def test_legacy_takes_priority_over_xdg(self):
        """Test that legacy directory takes priority when same app exists in both."""
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.fixtures_path, "xdg-config-home")

        config_files = ApplicationsDatabase.get_config_files()

        # Find the priority-test-app.cfg file
        priority_files = [f for f in config_files if "priority-test-app.cfg" in f]

        # Should only have one file (legacy should win)
        self.assertEqual(len(priority_files), 1)

        # Should be from legacy directory
        self.assertIn(".mackup", priority_files[0])
        self.assertNotIn("xdg-config-home", priority_files[0])

    def test_both_directories_merged(self):
        """Test that apps from both directories are available."""
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.fixtures_path, "xdg-config-home")

        config_files = ApplicationsDatabase.get_config_files()
        filenames = {os.path.basename(f) for f in config_files}

        # Both unique apps should be present
        self.assertIn("legacy-test-app.cfg", filenames)
        self.assertIn("xdg-test-app.cfg", filenames)

    def test_xdg_default_fallback(self):
        """Test that XDG falls back to ~/.config when XDG_CONFIG_HOME is not set."""
        # Unset XDG_CONFIG_HOME - should fall back to ~/.config
        os.environ.pop("XDG_CONFIG_HOME", None)

        # This test just verifies the code doesn't crash
        # In real scenario, ~/.config/mackup/applications/ would be checked
        config_files = ApplicationsDatabase.get_config_files()

        # Should at least contain stock apps and legacy custom apps
        self.assertTrue(len(config_files) > 0)

    def test_applications_database_loads_xdg_apps(self):
        """Test that ApplicationsDatabase correctly loads apps from XDG directory."""
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.fixtures_path, "xdg-config-home")

        db = ApplicationsDatabase()

        # XDG app should be loaded
        self.assertIn("xdg-test-app", db.get_app_names())
        self.assertEqual(db.get_name("xdg-test-app"), "XDG Test App")

    def test_applications_database_priority_loads_legacy(self):
        """Test that ApplicationsDatabase loads legacy version when app exists in both."""
        os.environ["XDG_CONFIG_HOME"] = os.path.join(self.fixtures_path, "xdg-config-home")

        db = ApplicationsDatabase()

        # Priority app should load the legacy version
        self.assertIn("priority-test-app", db.get_app_names())
        self.assertEqual(db.get_name("priority-test-app"), "Priority Test App Legacy")


if __name__ == "__main__":
    unittest.main()
