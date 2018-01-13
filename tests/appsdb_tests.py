import unittest
from nose.tools import raises
from mackup.appsdb import ApplicationsDatabase

class TestMackup(unittest.TestCase):

    def test_init(self):
        adb = ApplicationsDatabase()
        assert len(adb.apps) > 1

    def test_get_config(self):
        (source, cfg) =  ApplicationsDatabase.get_config("git")
        assert source == "core"

    @raises(SystemExit)
    def test_get_config_unknown(self):
        (source, cfg) =  ApplicationsDatabase.get_config("git-or-something")

    def test_get_names(self):
        adb = ApplicationsDatabase()
        names = adb.get_app_names()
        assert len(names) > 1
