import os
import os.path
import unittest
from pathlib import Path

from mackup.config import Config, ConfigError
from mackup.constants import (
    ENGINE_DROPBOX,
    ENGINE_FS,
    ENGINE_GDRIVE,
    ENGINE_ICLOUD,
    MACKUP_CONFIG_FILE,
)


def assert_correct_config_read(testtype):
    assert testtype == Config()._parser.get("test", "testtype")


class TestConfig(unittest.TestCase):
    def setUp(self):
        realpath = os.path.dirname(os.path.realpath(__file__))
        os.environ["HOME"] = os.path.join(realpath, "fixtures")

        # these may be set on some user's systems
        os.environ.pop("XDG_CONFIG_HOME", None)
        os.environ.pop("MACKUP_CONFIG", None)

    def test_config_envvar(self):
        os.environ["MACKUP_CONFIG"] = "~/mackup-envarcheck.cfg"
        assert_correct_config_read("test_config_envvar")

    def test_config_xdg(self):
        os.environ["XDG_CONFIG_HOME"] = "~/xdg-config-home/"
        assert_correct_config_read("test_config_xdg")

    def test_config_find_correct_default(self):
        config_path = Path.home() / MACKUP_CONFIG_FILE

        try:
            # create a default config file, this must be cleaned up after the test
            config_path.write_text("[test]\ntesttype = test_config_default")

            # nothing else set, should find the default file
            assert_correct_config_read("test_config_default")

            # set MACKUP_CONFIG, but should still find the default file
            os.environ["MACKUP_CONFIG"] = "~/mackup-envarcheck.cfg"
            assert_correct_config_read("test_config_default")

            # set XDG_CONFIG_HOME, but should still find the default file
            os.environ["XDG_CONFIG_HOME"] = "~/xdg-config-home/"
            assert_correct_config_read("test_config_default")
        except Exception:
            raise
        finally:
            config_path.unlink(missing_ok=True)

        assert config_path.exists() is False

    def test_config_finds_correct_envvar(self):
        # set XDG_CONFIG_HOME, but should still find the default file
        os.environ["XDG_CONFIG_HOME"] = "~/xdg-config-home/"
        assert_correct_config_read("test_config_xdg")

        # set MACKUP_CONFIG, but should still find the default file
        os.environ["MACKUP_CONFIG"] = "~/mackup-envarcheck.cfg"
        assert_correct_config_read("test_config_envvar")

    def test_config_no_config(self):
        cfg = Config()

        # Should should do the same as the default, empty configuration
        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        print(cfg.path)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/Mackup"

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_empty(self):
        cfg = Config("mackup-empty.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/Mackup"

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_engine_dropbox(self):
        cfg = Config("mackup-engine-dropbox.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "some_weirld_name"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/some_weirld_name"

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_engine_filesystem_absolute(self):
        cfg = Config("mackup-engine-file_system-absolute.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, str)
        assert cfg.path == "/some/absolute/folder"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "custom_folder"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/some/absolute/folder/custom_folder"

        assert cfg.apps_to_ignore == set(["subversion", "sequel-pro"])
        assert cfg.apps_to_sync == set()

    def test_config_engine_filesystem(self):
        cfg = Config("mackup-engine-file_system.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, str)
        assert cfg.path.endswith(
            os.path.join(os.environ["HOME"], "some/relative/folder")
        )

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == os.path.join(
            os.environ["HOME"], "some/relative/folder", "Mackup"
        )

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set(["sabnzbd", "sublime-text-3", "x11"])

    def test_config_engine_google_drive(self):
        cfg = Config("mackup-engine-google_drive.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_GDRIVE

        assert isinstance(cfg.path, str)
        assert cfg.path == "/Users/whatever/Google Drive"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath.endswith("/Google Drive/Mackup")

        assert cfg.apps_to_ignore == set(["subversion", "sequel-pro", "sabnzbd"])
        assert cfg.apps_to_sync == set(["sublime-text-3", "x11", "sabnzbd"])

    def test_config_engine_icloud(self):
        cfg = Config("mackup-engine-icloud.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_ICLOUD

        assert isinstance(cfg.path, str)
        assert cfg.path == os.path.expanduser(
            "~/Library/Mobile Documents/com~apple~CloudDocs/"
        )

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath.endswith("/com~apple~CloudDocs/Mackup")

        assert cfg.apps_to_ignore == set(["subversion", "sequel-pro", "sabnzbd"])
        assert cfg.apps_to_sync == set(["sublime-text-3", "x11", "sabnzbd"])

    def test_config_engine_filesystem_no_path(self):
        with self.assertRaises(ConfigError):
            Config("mackup-engine-file_system-no_path.cfg")

    def test_config_engine_unknown(self):
        with self.assertRaises(ConfigError):
            Config("mackup-engine-unknown.cfg")

    def test_config_apps_to_ignore(self):
        cfg = Config("mackup-apps_to_ignore.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/Mackup"

        assert cfg.apps_to_ignore == set(["subversion", "sequel-pro", "sabnzbd"])
        assert cfg.apps_to_sync == set()

    def test_config_apps_to_sync(self):
        cfg = Config("mackup-apps_to_sync.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/Mackup"

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set(["sabnzbd", "sublime-text-3", "x11"])

    def test_config_apps_to_ignore_and_sync(self):
        cfg = Config("mackup-apps_to_ignore_and_sync.cfg")

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == "/home/some_user/Dropbox"

        assert isinstance(cfg.directory, str)
        assert cfg.directory == "Mackup"

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == "/home/some_user/Dropbox/Mackup"

        assert cfg.apps_to_ignore == set(["subversion", "sequel-pro", "sabnzbd"])
        assert cfg.apps_to_sync == set(["sabnzbd", "sublime-text-3", "x11", "vim"])

    def test_config_old_config(self):
        self.assertRaises(SystemExit, Config, "mackup-old-config.cfg")
