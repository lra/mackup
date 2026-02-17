"""Tests for the --config-file command line option."""
import os
import unittest

import pytest

from mackup.config import Config
from mackup.mackup import Mackup


class TestConfigFileOption(unittest.TestCase):
    def setUp(self):
        realpath = os.path.dirname(os.path.realpath(__file__))
        os.environ["HOME"] = os.path.join(realpath, "fixtures")

        # Clear environment variables that could interfere
        os.environ.pop("XDG_CONFIG_HOME", None)
        os.environ.pop("MACKUP_CONFIG", None)

    def test_config_with_relative_path(self):
        """Test that a relative path to config file works."""
        cfg = Config("mackup-apps_to_ignore.cfg")

        assert cfg.apps_to_ignore == {"subversion", "sequel-pro", "sabnzbd"}

    def test_config_with_absolute_path(self):
        """Test that an absolute path to config file works."""
        abs_path = os.path.join(os.environ["HOME"], "mackup-apps_to_sync.cfg")
        cfg = Config(abs_path)

        assert cfg.apps_to_sync == {"sabnzbd", "sublime-text-3", "x11"}

    def test_mackup_with_config_file(self):
        """Test that Mackup class accepts config_file parameter."""
        # This should not raise any errors
        mckp = Mackup("mackup-empty.cfg")

        # Verify that the config was properly initialized
        assert mckp._config is not None
        assert isinstance(mckp.mackup_folder, str)

    def test_mackup_without_config_file(self):
        """Test that Mackup class works without config_file parameter."""
        # This should use default config file discovery
        mckp = Mackup()

        # Verify that the config was properly initialized
        assert mckp._config is not None
        assert isinstance(mckp.mackup_folder, str)

    def test_config_file_does_not_exist(self):
        """Test that specifying a non-existent config file raises an error."""
        with pytest.raises(SystemExit):
            Config("nonexistent-config-file.cfg")
