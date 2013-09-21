import os
import tempfile
import unittest

import mackup


class TestMackup(unittest.TestCase):

    def test_delete_file(self):
        # Create a tmp file
        tf = tempfile.NamedTemporaryFile(delete=False)
        tfpath = tf.name
        tf.close()

        # Make sure the created file exists
        assert os.path.isfile(tfpath)

        # Check if mackup can really delete it
        mackup.delete(tfpath)
        assert not os.path.exists(tfpath)

    def test_delete_folder_recursively(self):
        # Create a tmp folder
        tfpath = tempfile.mkdtemp()

        # Let's put a file in it just for fun
        tf = tempfile.NamedTemporaryFile(dir=tfpath, delete=False)
        filepath = tf.name
        tf.close()

        # Let's put another folder in it
        subfolder_path = tempfile.mkdtemp(dir=tfpath)

        # And a file in the subfolder
        tf = tempfile.NamedTemporaryFile(dir=subfolder_path, delete=False)
        subfilepath = tf.name
        tf.close()

        # Make sure the created files and folders exists
        assert os.path.isdir(tfpath)
        assert os.path.isfile(filepath)
        assert os.path.isdir(subfolder_path)
        assert os.path.isfile(subfilepath)

        # Check if mackup can really delete it
        mackup.delete(tfpath)
        assert not os.path.exists(tfpath)
        assert not os.path.exists(filepath)
        assert not os.path.exists(subfolder_path)
        assert not os.path.exists(subfilepath)
