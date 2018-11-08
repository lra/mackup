import unittest
import os.path
import tempfile

from mackup.constants import (ENGINE_DROPBOX,
                              ENGINE_GDRIVE,
                              ENGINE_COPY,
                              ENGINE_ICLOUD,
                              ENGINE_BOX,
                              ENGINE_FS,
                              MACKUP_CONFIG_FILE)
from mackup.config import Config, ConfigError


class TestConfig(unittest.TestCase):

    def setUp(self):
        realpath = os.path.dirname(os.path.realpath(__file__))
        os.environ['HOME'] = os.path.join(realpath, 'fixtures')

    def test_config_no_config(self):
        cfg = Config()

        # Should should do the same as the default, empty configuration
        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        print(cfg.path)
        assert cfg.path == '/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_empty(self):
        cfg = Config('mackup-empty.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_engine_dropbox(self):
        cfg = Config('mackup-engine-dropbox.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'some_weirld_name'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/some_weirld_name'

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_engine_filesystem_absolute(self):
        cfg = Config('mackup-engine-file_system-absolute.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/some/absolute/folder'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'custom_folder'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/some/absolute/folder/custom_folder'

        assert cfg.apps_to_ignore == set(['subversion', 'sequel-pro'])
        assert cfg.apps_to_sync == set()

    def test_config_engine_filesystem(self):
        cfg = Config('mackup-engine-file_system.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, str)
        assert cfg.path.endswith(os.path.join(os.environ[u'HOME'],
                                              u'some/relative/folder'))

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == os.path.join(os.environ[u'HOME'],
                                            u'some/relative/folder',
                                            u'Mackup')

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set(['sabnzbd', 'sublime-text-3', 'x11'])

    def test_config_engine_google_drive(self):
        cfg = Config('mackup-engine-google_drive.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_GDRIVE

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/Users/whatever/Google Drive'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath.endswith(u'/Google Drive/Mackup')

        assert cfg.apps_to_ignore == set(['subversion',
                                          'sequel-pro',
                                          'sabnzbd'])
        assert cfg.apps_to_sync == set(['sublime-text-3', 'x11', 'sabnzbd'])

    def test_config_engine_copy(self):
        cfg = Config('mackup-engine-copy.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_COPY

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/Users/someuser/Copy'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath.endswith(u'/Copy/Mackup')

        assert cfg.apps_to_ignore == set(['subversion',
                                          'sequel-pro',
                                          'sabnzbd'])
        assert cfg.apps_to_sync == set(['sublime-text-3', 'x11', 'sabnzbd'])

    def test_config_engine_icloud(self):
        cfg = Config('mackup-engine-icloud.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_ICLOUD

        assert isinstance(cfg.path, str)
        assert cfg.path == os.path.expanduser(
            '~/Library/Mobile Documents/com~apple~CloudDocs/')

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath.endswith(u'/com~apple~CloudDocs/Mackup')

        assert cfg.apps_to_ignore == set(['subversion',
                                          'sequel-pro',
                                          'sabnzbd'])
        assert cfg.apps_to_sync == set(['sublime-text-3', 'x11', 'sabnzbd'])

    def test_config_engine_box(self):
        cfg = Config('mackup-engine-box.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_BOX

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/Users/whatever/Box Sync'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'some_weirder_name'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/Users/whatever/Box Sync/some_weirder_name'

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set()

    def test_config_engine_filesystem_no_path(self):
        with self.assertRaises(ConfigError):
            Config('mackup-engine-file_system-no_path.cfg')

    def test_config_engine_unknown(self):
        with self.assertRaises(ConfigError):
            Config('mackup-engine-unknown.cfg')

    def test_config_apps_to_ignore(self):
        cfg = Config('mackup-apps_to_ignore.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == '/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

        assert cfg.apps_to_ignore == set(['subversion',
                                          'sequel-pro',
                                          'sabnzbd'])
        assert cfg.apps_to_sync == set()

    def test_config_apps_to_sync(self):
        cfg = Config('mackup-apps_to_sync.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

        assert cfg.apps_to_ignore == set()
        assert cfg.apps_to_sync == set(['sabnzbd',
                                        'sublime-text-3',
                                        'x11'])

    def test_config_apps_to_ignore_and_sync(self):
        cfg = Config('mackup-apps_to_ignore_and_sync.cfg')

        assert isinstance(cfg.engine, str)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, str)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, str)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, str)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

        assert cfg.apps_to_ignore == set(['subversion',
                                          'sequel-pro',
                                          'sabnzbd'])
        assert cfg.apps_to_sync == set(['sabnzbd',
                                        'sublime-text-3',
                                        'x11',
                                        'vim'])

    def test_config_old_config(self):
        self.assertRaises(SystemExit, Config, 'mackup-old-config.cfg')

    def test_default_config_path_returned_if_none_supplied(self):
        default_config_path = os.path.join(os.environ['HOME'],
                                           MACKUP_CONFIG_FILE)
        resolved_path = Config._resolve_config_path(None)

        assert resolved_path == default_config_path

    def test_resolves_config_path_relative_to_home_dir(self):
        base_dir = os.environ['HOME']

        with tempfile.NamedTemporaryFile(dir=base_dir) as config_file:
            relative_path = os.path.basename(config_file.name)
            resolved_path = Config._resolve_config_path(relative_path)

            assert resolved_path == config_file.name

    def test_resolves_config_path_relative_to_cwd(self):
        base_dir = os.getcwd()

        with tempfile.NamedTemporaryFile(dir=base_dir) as config_file:
            relative_path = os.path.basename(config_file.name)
            resolved_path = Config._resolve_config_path(relative_path)

            assert resolved_path == config_file.name

    def test_resolves_absolute_config_path(self):
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir:
            with tempfile.NamedTemporaryFile(dir=tmp_dir) as config_file:
                resolved_path = Config._resolve_config_path(config_file.name)

                assert resolved_path == config_file.name
