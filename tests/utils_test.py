import os
import tempfile
import unittest
import stat

# from unittest.mock import patch

from mackup import utils


class TestMackup(unittest.TestCase):

    def test_confirm_yes(self):
        # Override the raw_input used in utils
        def custom_raw_input(_):
            return 'Yes'
        utils.raw_input = custom_raw_input
        assert utils.confirm('Answer Yes to this question')

    def test_confirm_no(self):
        # Override the raw_input used in utils
        def custom_raw_input(_):
            return 'No'
        utils.raw_input = custom_raw_input
        assert not utils.confirm('Answer No to this question')

    def test_confirm_typo(self):
        # Override the raw_input used in utils
        def custom_raw_input(_):
            return 'No'
        utils.raw_input = custom_raw_input
        assert not utils.confirm('Answer garbage to this question')

    def test_delete_file(self):
        # Create a tmp file
        tf = tempfile.NamedTemporaryFile(delete=False)
        tfpath = tf.name
        tf.close()

        # Make sure the created file exists
        assert os.path.isfile(tfpath)

        # Check if mackup can really delete it
        utils.delete(tfpath)
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
        utils.delete(tfpath)
        assert not os.path.exists(tfpath)
        assert not os.path.exists(filepath)
        assert not os.path.exists(subfolder_path)
        assert not os.path.exists(subfilepath)

    def test_copy_file(self):
        # Create a tmp file
        tf = tempfile.NamedTemporaryFile(delete=False)
        srcfile = tf.name
        tf.close()

        # Create a tmp folder
        dstpath = tempfile.mkdtemp()
        # Set the destination filename
        dstfile = os.path.join(dstpath, "subfolder", os.path.basename(srcfile))

        # Make sure the source file and destination folder exist and the
        # destination file doesn't yet exist
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert not os.path.exists(dstfile)

        # Check if mackup can copy it
        utils.copy(srcfile, dstfile)
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert os.path.exists(dstfile)

        # Let's clean up
        utils.delete(dstpath)

    def test_copy_fail(self):
        # Create a tmp FIFO file
        tf = tempfile.NamedTemporaryFile()
        srcfile = tf.name
        tf.close()
        os.mkfifo(srcfile)

        # Create a tmp folder
        dstpath = tempfile.mkdtemp()
        # Set the destination filename
        dstfile = os.path.join(dstpath, "subfolder", os.path.basename(srcfile))

        # Make sure the source file and destination folder exist and the
        # destination file doesn't yet exist
        assert not os.path.isfile(srcfile)
        assert stat.S_ISFIFO(os.stat(srcfile).st_mode)
        assert os.path.isdir(dstpath)
        assert not os.path.exists(dstfile)

        # Check if mackup can copy it
        self.assertRaises(ValueError, utils.copy, srcfile, dstfile)
        assert not os.path.isfile(srcfile)
        assert stat.S_ISFIFO(os.stat(srcfile).st_mode)
        assert os.path.isdir(dstpath)
        assert not os.path.exists(dstfile)

        # Let's clean up
        utils.delete(srcfile)
        utils.delete(dstpath)

    def test_copy_dir(self):
        # Create a tmp folder
        srcpath = tempfile.mkdtemp()

        # Create a tmp file
        tf = tempfile.NamedTemporaryFile(delete=False, dir=srcpath)
        srcfile = tf.name
        tf.close()

        # Create a tmp folder
        dstpath = tempfile.mkdtemp()

        # Set the destination filename
        srcpath_basename = os.path.basename(srcpath)
        dstfile = os.path.join(dstpath,
                               'subfolder',
                               srcpath_basename,
                               os.path.basename(srcfile))
        # Make sure the source file and destination folder exist and the
        # destination file doesn't yet exist
        assert os.path.isdir(srcpath)
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert not os.path.exists(dstfile)

        # Check if mackup can copy it
        utils.copy(srcfile, dstfile)
        assert os.path.isdir(srcpath)
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert os.path.exists(dstfile)

        # Let's clean up
        utils.delete(srcpath)
        utils.delete(dstpath)

    def test_link_file(self):
        # Create a tmp file
        tf = tempfile.NamedTemporaryFile(delete=False)
        srcfile = tf.name
        tf.close()

        # Create a tmp folder
        dstpath = tempfile.mkdtemp()
        # Set the destination filename
        dstfile = os.path.join(dstpath, "subfolder", os.path.basename(srcfile))

        # Make sure the source file and destination folder exist and the
        # destination file doesn't yet exist
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert not os.path.exists(dstfile)

        # Check if mackup can link it and the link points to the correct place
        utils.link(srcfile, dstfile)
        assert os.path.isfile(srcfile)
        assert os.path.isdir(dstpath)
        assert os.path.exists(dstfile)
        assert os.readlink(dstfile) == srcfile

        # Let's clean up
        utils.delete(dstpath)
