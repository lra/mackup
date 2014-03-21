"""System static utilities being used by the modules"""
import argparse
import base64
import os
import platform
import shutil
import stat
import subprocess
import sys
import sqlite3

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
              " - backup: sync your conf files to your synced storage, use"
              " this the 1st time you use Mackup.\n"
              " - restore: link the conf files already in your synced storage"
              " on your system, use it on any new system you use.\n"
              " - uninstall: reset everything as it was before using Mackup.\n"
              " - list: display a list of all supported applications.\n"
              " - enable: enables apps in the config file\n"
              " - disable: disables the apps in the config file\n")

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
                                 constants.LIST_MODE,
                                 constants.ENABLE_MODE,
                                 constants.DISABLE_MODE,],
                        help=help_msg)
    # Get the list of apps for DISABLE/ENABLE mode
    parser.add_argument("apps", nargs = argparse.REMAINDER, help=("The list "
                       "of apps used in the enable/disable commands"))

    # Parse the command line and return the parsed options
    return parser.parse_args()


def get_dropbox_folder_location():
    """
    Try to locate the Dropbox folder

    Returns:
        (str) Full path to the current Dropbox folder
    """
    host_db_path = os.path.join(os.environ['HOME'], '.dropbox/host.db')
    try:
        with open(host_db_path, 'r') as f_hostdb:
            data = f_hostdb.read().split()
    except IOError:
        error("Unable to find your Dropbox install =(")
    dropbox_home = base64.b64decode(data[1])

    return dropbox_home


def get_google_drive_folder_location():
    """
    Try to locate the Google Drive folder

    Returns:
        (unicode) Full path to the current Google Drive folder
    """
    gdrive_db_path = 'Library/Application Support/Google/Drive/sync_config.db'
    googledrive_home = None

    gdrive_db = os.path.join(os.environ['HOME'], gdrive_db_path)
    if (os.path.isfile(gdrive_db)):
        con = sqlite3.connect(gdrive_db)
        if con:
            cur = con.cursor()
            query = ("SELECT data_value "
                     "FROM data "
                     "WHERE entry_key = 'local_sync_root_path';")
            cur.execute(query)
            data = cur.fetchone()
            googledrive_home = unicode(data[0])
            con.close()

    if not googledrive_home:
        error("Unable to find your Google Drive install =(")

    return googledrive_home


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


def append_to_config(config, section, apps):
    """
    Writes the apps to the section in the config file. If the section is not
    in the config it is created

    Args:
        (Config): The config object that is used in mackup which implements a
                  (safe) config parser
        (str): The section where the apps will be written to in the config file
               Do NOT include the brackets
        (iterable): The apps to be written to the config file
    """
    config_path = os.path.join(os.environ['HOME'],
                               constants.MACKUP_CONFIG_FILE)
    for app in apps:
        # Double check that each app is not already ignored or synced
        # We parse the configuration file again because it might have changed
        if app in config._apps_to_sync.union(config._apps_to_ignore):
            error("{} is approved to be {} according to {}".format(
            app, "synced" if app in config._apps_to_sync else "ignored",
            config_path))
    # If that section is not in the config file, add it
    # Bad sections aren't checked, because it wouldn't affect mackup
    if not config._parser.has_section(section):
        config._parser.add_section(section)
        with open(config_path, "w") as config_file:
            config._parser.write(config_file)
    # Get all the text in the config file first
    with open(os.path.join(os.environ['HOME'], constants.MACKUP_CONFIG_FILE),
              "r") as config_file:
        text = config_file.readlines()
    # Write the apps to the config file
    with open(config_path, "r+") as config_file:
        for line in text:
            config_file.write(line)
            # Find where the section starts
            if line == "[" + section + "]\n":
                config_file.writelines(apps)
                # Write extra line so it can be parsed properly (yes hacky)
                config_file.write("\n")


def clean_config_file(apps):
    """
    Clears all instances of any of the apps in the config file. This should be
    ran before appending the apps to the config file due to unforeseeable bugs

    Args:
        (iterable): The apps that will be purged from the config file
    """
    # Get all the text in the config file first
    with open(os.path.join(os.environ['HOME'], constants.MACKUP_CONFIG_FILE),
              "r") as config_file:
        text = config_file.readlines()
    # Rewrite to the config file
    with open(os.path.join(os.environ['HOME'],
               constants.MACKUP_CONFIG_FILE), "w") as config_file:
        for line in text:
            # Ignore any lines that have one of the apps in it
            if line not in (app + "\n" for app in apps):
                config_file.write(line)
