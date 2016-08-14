from mackup import application, mackup

import mock
import unittest
import os
import shutil
import tempfile
import contextlib


class TestApplicationProfile(unittest.TestCase):

    def setUp(self):
        self.fake_home = tempfile.mkdtemp()
        self.fake_mackup = os.path.join(self.fake_home, 'mackup')

        # Fake home path.
        os.environ['HOME'] = self.fake_home

        # mackup/home file path for testing
        filename = 'test.rc'
        self.home_filepath = self.prepend_home_path(filename)
        self.mackup_filepath = self.prepend_mackup_path(filename)

        # Mock mackup
        mckp = mock.MagicMock(spec=mackup.Mackup)
        mckp.mackup_folder = self.fake_mackup

        self.app = application.ApplicationProfile(mckp, {filename},
                                                  dry_run=False,
                                                  verbose=False)

    def tearDown(self):
        shutil.rmtree(self.fake_home)

    @staticmethod
    def create_file(filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'w') as f:
            f.write('this is a test file')

    @staticmethod
    @contextlib.contextmanager
    def confirm(answer):
        with mock.patch('mackup.utils.confirm') as confirm:
            confirm.return_value = answer
            yield

    def prepend_home_path(self, filename):
        return os.path.join(self.fake_home, filename)

    def prepend_mackup_path(self, filename):
        return os.path.join(self.fake_mackup, filename)

    def test_restore_without_home_file(self):
        self.create_file(self.mackup_filepath)
        self.app.restore()

        self.assertTrue(os.path.islink(self.home_filepath))
        self.assertTrue(os.path.exists(self.home_filepath))
        self.assertTrue(os.path.samefile(self.home_filepath, self.mackup_filepath))

    def test_restore_with_pointing_to_mackup(self):
        self.create_file(self.mackup_filepath)
        os.symlink(self.mackup_filepath, self.home_filepath)

        with self.confirm(True):
            self.app.restore()

        self.assertTrue(os.path.exists(self.home_filepath))
        self.assertTrue(os.path.exists(self.mackup_filepath))
        self.assertTrue(os.path.samefile(self.home_filepath, self.mackup_filepath))

    def test_restore_broken_link(self):
        self.create_file(self.mackup_filepath)
        os.symlink('broken_link', self.home_filepath)

        # home_filepath should be a broken link
        assert(os.path.islink(self.home_filepath) and
               not os.path.exists(self.home_filepath))

        with self.confirm(False):
            self.app.restore()

        self.assertTrue(os.path.islink(self.home_filepath) and
                        not os.path.exists(self.home_filepath))

        with self.confirm(True):
            self.app.restore()

        self.assertTrue(os.path.islink(self.home_filepath) and
                        os.path.exists(self.home_filepath))
        self.assertTrue(os.path.samefile(self.home_filepath, self.mackup_filepath))

    def test_restore_pointing_to_other(self):
        other_filepath = self.prepend_home_path('other_file')
        self.create_file(self.mackup_filepath)
        self.create_file(other_filepath)
        os.symlink(other_filepath, self.home_filepath)

        assert(not os.path.samefile(other_filepath, self.mackup_filepath))
        assert(os.path.samefile(other_filepath, self.home_filepath))

        with self.confirm(False):
            self.app.restore()

        self.assertFalse(os.path.samefile(other_filepath, self.mackup_filepath))
        self.assertTrue(os.path.samefile(other_filepath, self.home_filepath))

        with self.confirm(True):
            self.app.restore()

        self.assertFalse(os.path.samefile(self.home_filepath, other_filepath))
        self.assertTrue(os.path.samefile(self.mackup_filepath, self.home_filepath))

    def test_restore_other_file(self):
        self.create_file(self.home_filepath)
        self.create_file(self.mackup_filepath)

        assert(not os.path.samefile(self.home_filepath, self.mackup_filepath))

        with self.confirm(False):
            self.app.restore()

        self.assertFalse(os.path.samefile(self.home_filepath, self.mackup_filepath))

        with self.confirm(True):
            self.app.restore()

        self.assertTrue(os.path.samefile(self.home_filepath, self.mackup_filepath))
        self.assertTrue(os.path.islink(self.home_filepath))
