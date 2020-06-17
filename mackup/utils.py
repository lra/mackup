"""System static utilities being used by the modules."""
import base64
import os
import platform
import shutil
import sqlite3
import stat
import subprocess
import sys

from six.moves import input

from . import constants

# Flag that controls how user confirmation works.
# If True, the user wants to say "yes" to everything.
FORCE_YES = False

# Flag that control if mackup can be run as root
CAN_RUN_AS_ROOT = False


def confirm(question):
    """
    Ask the user if he really want something to happen.

    Args:
        question(str): What can happen

    Returns:
        (boolean): Confirmed or not
    """
    if FORCE_YES:
        return True

    while True:
        answer = input(question + ' <Yes|No>').lower()

        if answer == 'yes' or answer == 'y':
            confirmed = True
            break
        if answer == 'no' or answer == 'n':
            confirmed = False
            break

    return confirmed


def delete(filepath):
    """
    Delete the given file, directory or link.

    It Should support undelete later on.

    Args:
        filepath (str): Absolute full path to a file. e.g. /path/to/file
    """
    # Some files have ACLs, let's remove them recursively
    remove_acl(filepath)

    # Some files have immutable attributes, let's remove them recursively
    remove_immutable_attribute(filepath)

    # Finally remove the files and folders
    if os.path.isfile(filepath) or os.path.islink(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


def copy(src, dst):
    """
    Copy a file or a folder (recursively) from src to dst.

    For simplicity sake, both src and dst must be absolute path and must
    include the filename of the file or folder.
    Also do not include any trailing slash.

    e.g. copy('/path/to/src_file', '/path/to/dst_file')
    or copy('/path/to/src_folder', '/path/to/dst_folder')

    But not: copy('/path/to/src_file', 'path/to/')
    or copy('/path/to/src_folder/', '/path/to/dst_folder')

    Args:
        src (str): Source file or folder
        dst (str): Destination file or folder
    """
    assert isinstance(src, str)
    assert os.path.exists(src)
    assert isinstance(dst, str)

    # Create the path to the dst file if it does not exists
    abs_path = os.path.dirname(os.path.abspath(dst))
    if not os.path.isdir(abs_path):
        os.makedirs(abs_path)

    # We need to copy a single file
    if os.path.isfile(src):
        # Copy the src file to dst
        shutil.copy(src, dst)

    # We need to copy a whole folder
    elif os.path.isdir(src):
        shutil.copytree(src, dst)

    # What the heck is this ?
    else:
        raise ValueError("Unsupported file: {}".format(src))

    # Set the good mode to the file or folder recursively
    chmod(dst)


def link(target, link_to, physical=False):
    """
    Create a link to a target file or a folder.

    For simplicity sake, both target and link_to must be absolute path and must
    include the filename of the file or folder.
    Also do not include any trailing slash.

    e.g. link('/path/to/file', '/path/to/link')

    But not: link('/path/to/file', 'path/to/')
    or link('/path/to/folder/', '/path/to/link')

    Args:
        target (str): file or folder the link will point to
        link_to (str): Link to create
        physical (bool):
    """
    assert isinstance(target, str)
    assert os.path.exists(target)
    assert isinstance(link_to, str)

    # Create the path to the link if it does not exists
    abs_path = os.path.dirname(os.path.abspath(link_to))
    if not os.path.isdir(abs_path):
        os.makedirs(abs_path)

    # Make sure the file or folder recursively has the good mode
    chmod(target)

    # Create the link to target
    if physical:
        if os.path.isdir(target):
            copytree(target, link_to, copy_function=os.link)
        else:
            os.link(target, link_to)
    else:
        os.symlink(target, link_to)


def chmod(target):
    """
    Recursively set the chmod for files to 0600 and 0700 for folders.

    It's ok unless we need something more specific.

    Args:
        target (str): Root file or folder
    """
    assert isinstance(target, str)
    assert os.path.exists(target)

    file_mode = stat.S_IRUSR | stat.S_IWUSR
    folder_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR

    # Remove the immutable attribute recursively if there is one
    remove_immutable_attribute(target)

    if os.path.isfile(target):
        os.chmod(target, file_mode)

    elif os.path.isdir(target):
        # chmod the root item
        os.chmod(target, folder_mode)

        # chmod recursively in the folder it it's one
        for root, dirs, files in os.walk(target):
            for cur_dir in dirs:
                os.chmod(os.path.join(root, cur_dir), folder_mode)
            for cur_file in files:
                os.chmod(os.path.join(root, cur_file), file_mode)

    else:
        raise ValueError("Unsupported file type: {}".format(target))


def error(message):
    """
    Throw an error with the given message and immediately quit.

    Args:
        message(str): The message to display.
    """
    fail = '\033[91m'
    end = '\033[0m'
    sys.exit(fail + "Error: {}".format(message) + end)


def get_dropbox_folder_location():
    """
    Try to locate the Dropbox folder.

    Returns:
        (str) Full path to the current Dropbox folder
    """
    host_db_path = os.path.join(os.environ['HOME'], '.dropbox/host.db')
    try:
        with open(host_db_path, 'r') as f_hostdb:
            data = f_hostdb.read().split()
    except IOError:
        error("Unable to find your Dropbox install =(")
    dropbox_home = base64.b64decode(data[1]).decode()

    return dropbox_home


def get_google_drive_folder_location():
    """
    Try to locate the Google Drive folder.

    Returns:
        (str) Full path to the current Google Drive folder
    """
    gdrive_db_path = 'Library/Application Support/Google/Drive/sync_config.db'
    yosemite_gdrive_db_path = ('Library/Application Support/Google/Drive/'
                               'user_default/sync_config.db')
    yosemite_gdrive_db = os.path.join(os.environ['HOME'],
                                      yosemite_gdrive_db_path)
    if os.path.isfile(yosemite_gdrive_db):
        gdrive_db_path = yosemite_gdrive_db

    googledrive_home = None

    gdrive_db = os.path.join(os.environ['HOME'], gdrive_db_path)
    if os.path.isfile(gdrive_db):
        con = sqlite3.connect(gdrive_db)
        if con:
            cur = con.cursor()
            query = ("SELECT data_value "
                     "FROM data "
                     "WHERE entry_key = 'local_sync_root_path';")
            cur.execute(query)
            data = cur.fetchone()
            googledrive_home = str(data[0])
            con.close()

    if not googledrive_home:
        error("Unable to find your Google Drive install =(")

    return googledrive_home


def get_copy_folder_location():
    """
    Try to locate the Copy folder.

    Returns:
        (str) Full path to the current Copy folder
    """
    copy_settings_path = 'Library/Application Support/Copy Agent/config.db'
    copy_home = None

    copy_settings = os.path.join(os.environ['HOME'], copy_settings_path)

    if os.path.isfile(copy_settings):
        database = sqlite3.connect(copy_settings)
        if database:
            cur = database.cursor()
            query = ("SELECT value "
                     "FROM config2 "
                     "WHERE option = 'csmRootPath';")
            cur.execute(query)
            data = cur.fetchone()
            copy_home = str(data[0])
            cur.close()

    if not copy_home:
        error("Unable to find your Copy install =(")

    return copy_home


def get_icloud_folder_location():
    """
    Try to locate the iCloud Drive folder.

    Returns:
        (str) Full path to the iCloud Drive folder.
    """
    yosemite_icloud_path = '~/Library/Mobile Documents/com~apple~CloudDocs/'

    icloud_home = os.path.expanduser(yosemite_icloud_path)

    if not os.path.isdir(icloud_home):
        error('Unable to find your iCloud Drive =(')

    return str(icloud_home)


def is_process_running(process_name):
    """
    Check if a process with the given name is running.

    Args:
        (str): Process name, e.g. "Sublime Text"

    Returns:
        (bool): True if the process is running
    """
    is_running = False

    # On systems with pgrep, check if the given process is running
    if os.path.isfile('/usr/bin/pgrep'):
        dev_null = open(os.devnull, 'wb')
        returncode = subprocess.call(['/usr/bin/pgrep', process_name],
                                     stdout=dev_null)
        is_running = bool(returncode == 0)

    return is_running


def remove_acl(path):
    """
    Remove the ACL of the file or folder located on the given path.

    Also remove the ACL of any file and folder below the given one,
    recursively.

    Args:
        path (str): Path to the file or folder to remove the ACL for,
                    recursively.
    """
    # Some files have ACLs, let's remove them recursively
    if (platform.system() == constants.PLATFORM_DARWIN and
            os.path.isfile('/bin/chmod')):
        subprocess.call(['/bin/chmod', '-R', '-N', path])
    elif ((platform.system() == constants.PLATFORM_LINUX) and
            os.path.isfile('/bin/setfacl')):
        subprocess.call(['/bin/setfacl', '-R', '-b', path])


def remove_immutable_attribute(path):
    """
    Remove the immutable attribute of the given path.

    Remove the immutable attribute of the file or folder located on the given
    path. Also remove the immutable attribute of any file and folder below the
    given one, recursively.

    Args:
        path (str): Path to the file or folder to remove the immutable
                    attribute for, recursively.
    """
    # Some files have ACLs, let's remove them recursively
    if platform.system() == constants.PLATFORM_DARWIN and
            os.path.isfile('/usr/bin/chflags'):
        subprocess.call(['/usr/bin/chflags', '-R', 'nouchg', path])
    elif platform.system() == constants.PLATFORM_LINUX and
            os.path.isfile('/usr/bin/chattr'):
        subprocess.call(['/usr/bin/chattr', '-R', '-f', '-i', path])


def can_file_be_synced_on_current_platform(path):
    """
    Check if the given path can be synced locally.

    Check if it makes sense to sync the file at the given path on the current
    platform.
    For now we don't sync any file in the ~/Library folder on GNU/Linux.
    There might be other exceptions in the future.

    Args:
        (str): Path to the file or folder to check. If relative, prepend it
               with the home folder.
               'abc' becomes '~/abc'
               '/def' stays '/def'

    Returns:
        (bool): True if given file can be synced
    """
    can_be_synced = True

    # If the given path is relative, prepend home
    fullpath = os.path.join(os.environ['HOME'], path)

    # Compute the ~/Library path on OS X
    # End it with a slash because we are looking for this specific folder and
    # not any file/folder named LibrarySomething
    library_path = os.path.join(os.environ['HOME'], 'Library/')

    if platform.system() == constants.PLATFORM_LINUX:
        if fullpath.startswith(library_path):
            can_be_synced = False

    return can_be_synced


def copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2,
             ignore_dangling_symlinks=False):
    """Recursively copy a directory tree.

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.

    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():

        callable(src, names) -> ignored_names

    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.

    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.islink(srcname):
                linkto = os.readlink(srcname)
                if symlinks:
                    # We can't just leave it to `copy_function` because legacy
                    # code with a custom `copy_function` may rely on copytree
                    # doing the right thing.
                    os.symlink(linkto, dstname)
                    shutil.copystat(srcname, dstname, follow_symlinks=not symlinks)
                else:
                    # ignore dangling symlink if the flag is on
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    # otherwise let the copy occurs. copy2 will raise an error
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname, symlinks, ignore,
                                 copy_function)
                    else:
                        copy_function(srcname, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore, copy_function)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy_function(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)
    return dst
