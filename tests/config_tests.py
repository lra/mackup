import unittest
import os.path

from mackup.constants import (ENGINE_DROPBOX,
                              ENGINE_GDRIVE,
                              ENGINE_FS)
from mackup.config import Config, ConfigError
from mackup import utils


class TestConfig(unittest.TestCase):

    def setUp(self):
        realpath = os.path.dirname(os.path.realpath(__file__))
        os.environ['HOME'] = os.path.join(realpath, 'fixtures')


    def test_config_empty(self):
        cfg = Config('mackup-empty.cfg')

        assert isinstance(cfg.engine, unicode)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, unicode)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, unicode)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, unicode)
        assert cfg.fullpath == u'/home/some_user/Dropbox/Mackup'

    def test_config_engine_dropbox(self):
        cfg = Config('mackup-engine-dropbox.cfg')

        assert isinstance(cfg.engine, unicode)
        assert cfg.engine == ENGINE_DROPBOX

        assert isinstance(cfg.path, unicode)
        assert cfg.path == u'/home/some_user/Dropbox'

        assert isinstance(cfg.directory, unicode)
        assert cfg.directory == u'some_weirld_name'

        assert isinstance(cfg.fullpath, unicode)
        assert cfg.fullpath == u'/home/some_user/Dropbox/some_weirld_name'

    def test_config_engine_filesystem_absolute(self):
        cfg = Config('mackup-engine-file_system-absolute.cfg')

        assert isinstance(cfg.engine, unicode)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, unicode)
        assert cfg.path == u'/some/absolute/folder'

        assert isinstance(cfg.directory, unicode)
        assert cfg.directory == u'custom_folder'

        assert isinstance(cfg.fullpath, unicode)
        assert cfg.fullpath == u'/some/absolute/folder/custom_folder'

    def test_config_engine_filesystem(self):
        cfg = Config('mackup-engine-file_system.cfg')

        assert isinstance(cfg.engine, unicode)
        assert cfg.engine == ENGINE_FS

        assert isinstance(cfg.path, unicode)
        assert cfg.path.endswith(os.path.join(os.environ[u'HOME'],
                                              u'some/relative/folder'))

        assert isinstance(cfg.directory, unicode)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, unicode)
        assert cfg.fullpath == os.path.join(os.environ[u'HOME'],
                                            u'some/relative/folder',
                                            u'Mackup')

    def test_config_engine_google_drive(self):
        cfg = Config('mackup-engine-google_drive.cfg')

        assert isinstance(cfg.engine, unicode)
        assert cfg.engine == ENGINE_GDRIVE

        assert isinstance(cfg.path, unicode)
        assert cfg.path == u'/Users/whatever/Google Drive'

        assert isinstance(cfg.directory, unicode)
        assert cfg.directory == u'Mackup'

        assert isinstance(cfg.fullpath, unicode)
        assert cfg.fullpath.endswith(u'/Google Drive/Mackup')

    def test_config_engine_filesystem_no_path(self):
        with self.assertRaises(ConfigError):
            Config('mackup-engine-file_system-no_path.cfg')

    def test_config_engine_unknown(self):
        with self.assertRaises(ConfigError):
            Config('mackup-engine-unknown.cfg')
