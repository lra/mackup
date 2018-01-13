import unittest
from nose.tools import raises
from mackup import mackup

class TestMackup(unittest.TestCase):

    def test_mackup_header(self):
        assert mackup.header('blah') == '\033[34mblah\033[0m'

    def test_main_bold(self):
        assert mackup.bold('blah') == '\033[1mblah\033[0m'

    def test_mackup_create(self):
        mckp = mackup.Mackup()
        assert mckp.dry_run == False
        assert mckp.verbose == False

    @raises(SystemExit)
    def test_envs(self):
        mckp = mackup.Mackup()
        mckp.check_environment()

    @raises(SystemExit)
    def test_ops_envs(self):
        mckp = mackup.Mackup()
        def mock_check():
            return True
        mckp.check_environment =  mock_check
        mckp.create_mackup_home = mock_check

        mckp.check_backup_env()
        mckp.check_restore_env()

    def test_get_apps_to_backup(self):
        mckp = mackup.Mackup()
        apps = mckp.get_apps_to_backup()
        assert len(apps) > 1
