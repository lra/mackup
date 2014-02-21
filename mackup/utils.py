"""System static utilities being used by the modules"""
import argparse
import base64
import os
import platform
import shutil
import stat
import subprocess
import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from . import appsdb
from . import constants


def confirm(question):
    """
    Ask the user if he really want something to happen

    Args:
        question(str): What can happen

    Returns:
        (boolean): Confirmed or not
    """
    while True:
        answer = raw_input(question + ' <Yes|No>')
        if answer == 'Yes':
            confirmed = True
            break
        if answer == 'No':
            confirmed = False
            break

    return confirmed


def delete(filepath):
    """
    Delete the given file, directory or link.
    Should support undelete later on.

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


def link(target, link):
    """
    Create a link to a target file or a folder.
    For simplicity sake, both target and link must be absolute path and must
    include the filename of the file or folder.
    Also do not include any trailing slash.

    e.g. link('/path/to/file', '/path/to/link')

    But not: link('/path/to/file', 'path/to/')
    or link('/path/to/folder/', '/path/to/link')

    Args:
        target (str): file or folder the link will point to
        link (str): Link to create
    """
    assert isinstance(target, str)
    assert os.path.exists(target)
    assert isinstance(link, str)

    # Create the path to the link if it does not exists
    abs_path = os.path.dirname(os.path.abspath(link))
    if not os.path.isdir(abs_path):
        os.makedirs(abs_path)

    # Make sure the file or folder recursively has the good mode
    chmod(target)

    # Create the link to target
    os.symlink(target, link)


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
    sys.exit("Error: {}".format(message))


def parse_cmdline_args():
    """
    Setup the engine that's gonna parse the command line arguments

    Returns:
        (argparse.Namespace)
    """

    # Format the description text
    description = ("Mackup {}\n"
                   "Keep your application settings in sync.\n"
                   "Copyright (C) 2013-2014 Laurent Raufaste"
                   " <http://glop.org/>\n"
                   .format(constants.VERSION))

    # Format some epilog text
    epilog = ("Mackup modes of action:\n"
              " - backup: sync your conf files to Dropbox, use this the 1st"
              " time you use Mackup.\n"
              " - restore: link the conf files already in Dropbox on your "
              " system, use it on any new system you use.\n"
              " - uninstall: reset everything as it was before using Mackup.\n"
              " - list: display a list of all supported applications.\n"
              "\n"
              "Mackup requires a fully synced Dropbox folder.")

    help_msg = "Required action mode for Mackup, see below for details."

    # Setup the global parser
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Add the required arg
    parser.add_argument("mode",
                        choices=[constants.BACKUP_MODE,
                                 constants.RESTORE_MODE,
                                 constants.UNINSTALL_MODE,
                                 constants.LIST_MODE],
                        help=help_msg)

    # Parse the command line and return the parsed options
    return parser.parse_args()


def get_dropbox_folder_location():
    """
    Try to locate the Dropbox folder

    Returns:
        (str) Full path to the current Dropbox folder
    """
    if os.environ.has_key("MACKUP_DROPBOX_HOST_DB"):
        host_db_path = os.path.expanduser(os.path.expandvars(os.environ['MACKUP_DROPBOX_HOST_DB']))
    else:
        host_db_path = os.environ['HOME'] + '/.dropbox/host.db'

    with open(host_db_path, 'r') as f_hostdb:
        data = f_hostdb.read().split()
    dropbox_home = base64.b64decode(data[1])

    return dropbox_home


def get_ignored_apps():
    """
    Get the list of applications ignored in the config file

    Returns:
        (set) List of application names to ignore, lowercase
    """
    # If a config file exists, grab it and parser it
    config = configparser.SafeConfigParser(allow_no_value=True)

    # We ignore nothing by default
    ignored_apps = []

    # Is the config file there ?
    path_to_cfg = "{}/{}".format(os.environ['HOME'],
                                 constants.MACKUP_CONFIG_FILE)
    if config.read(path_to_cfg):
        # Is the "[applications_to_ignore]" in the cfg file ?
        if config.has_section('applications_to_ignore'):
            ignored_apps = config.options('applications_to_ignore')

    return set(ignored_apps)


def get_allowed_apps():
    """
    Get the list of applications allowed in the config file

    Returns:
        (list) list of application names to backup
    """

    # Instantiate the app db
    app_db = appsdb.ApplicationsDatabase()

    # If a config file exists, grab it and parser it
    config = configparser.SafeConfigParser(allow_no_value=True)

    # We allow all by default
    allowed_apps = app_db.get_app_names()

    # Is the config file there ?
    path_to_cfg = "{}/{}".format(os.environ['HOME'],
                                 constants.MACKUP_CONFIG_FILE)
    if config.read(path_to_cfg):
        # Is the "[applications_to_sync]" section in the cfg file ?
        if config.has_section('applications_to_sync'):
            # Reset allowed apps to include only the user-defined
            allowed_apps = []
            for app_name in app_db.get_app_names():
                if app_name in config.options('applications_to_sync'):
                    allowed_apps.append(app_name)

    return allowed_apps


def get_apps_to_backup():
    """
    Get the list of application that should be backup by Mackup.
    It's the list of allowed apps minus the list of ignored apps.

    Returns:
        (set) List of application names to backup
    """
    apps_to_backup = []
    apps_to_ignore = get_ignored_apps()
    apps_to_allow = get_allowed_apps()

    for app_name in apps_to_allow:
        if app_name not in apps_to_ignore:
            apps_to_backup.append(app_name)

    return apps_to_backup


def is_process_running(process_name):
    """
    Check if a process with the given name is running

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
    if (platform.system() == constants.PLATFORM_DARWIN
        and os.path.isfile('/bin/chmod')):
        subprocess.call(['/bin/chmod', '-R', '-N', path])
    elif ((platform.system() == constants.PLATFORM_LINUX)
          and os.path.isfile('/bin/setfacl')):
        subprocess.call(['/bin/setfacl', '-R', '-b', path])


def remove_immutable_attribute(path):
    """
    Remove the immutable attribute of the file or folder located on the given
    path. Also remove the immutable attribute of any file and folder below the
    given one, recursively.

    Args:
        path (str): Path to the file or folder to remove the immutable
                    attribute for, recursively.
    """
    # Some files have ACLs, let's remove them recursively
    if ((platform.system() == constants.PLATFORM_DARWIN)
        and os.path.isfile('/usr/bin/chflags')):
        subprocess.call(['/usr/bin/chflags', '-R', 'nouchg', path])
    elif (platform.system() == constants.PLATFORM_LINUX
          and os.path.isfile('/usr/bin/chattr')):
        subprocess.call(['/usr/bin/chattr', '-R', '-i', path])


def can_file_be_synced_on_current_platform(path):
    """
    Check if it makes sens to sync the file at the given path on the current
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
