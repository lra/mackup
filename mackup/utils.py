"""System static utilities being used by the modules."""
import base64
import difflib
import filecmp
import json
import os
import platform
import plistlib
import pprint
import re
import shutil
import stat
import subprocess
import sys
import sqlite3
import textwrap
from typing import Tuple, Optional

from six.moves import input

from . import constants
from .colors import magenta, red, warning_log, info_log

# Flag that controls how user confirmation works.
# If True, the user wants to say "yes" to everything.
FORCE_YES = False

# Flag that control if mackup can be run as root
CAN_RUN_AS_ROOT = False

# Flag that controls whether we should copy the files rather than create symlinks
SHOULD_COPY = False

# Whether verbose logging is enabled
VERBOSE = False

# Whether dry-run mode is enabled
DRY_RUN = False


def vlog(message: str) -> None:
    """ Print a message if VERBOSE is true """
    if VERBOSE:
        print(magenta(message))


def confirm(question: str) -> bool:
    """
    Ask the user if he really wants something to happen.

    Args:
        question(str): What can happen

    Returns:
        (boolean): Confirmed or not
    """
    if FORCE_YES:
        return True

    while True:
        try:
            answer = input(question + " <Yes|No> ").lower()
        except KeyboardInterrupt:
            warning_log("\nExiting gracefully...")
            sys.exit(0)

        if answer == "yes" or answer == "y":
            confirmed = True
            break
        if answer == "no" or answer == "n":
            confirmed = False
            break

    return confirmed


def delete(filepath: str) -> None:
    """
    Delete the given file, directory or link.

    It Should support undelete later on.

    Args:
        filepath (str): Absolute full path to a file. e.g. /path/to/file
    """
    if DRY_RUN:
        warning_log(f"dry-run: Would have deleted {filepath}")
        return

    # Some files have ACLs, let's remove them recursively
    remove_acl(filepath)

    # Some files have immutable attributes, let's remove them recursively
    remove_immutable_attribute(filepath)

    # Finally remove the files and folders
    if os.path.isfile(filepath) or os.path.islink(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


def copy(src: str, dst: str) -> None:
    """
    Copy a file or a folder (recursively) from src to dst.

    For the sake of simplicity, both src and dst must be absolute path and must
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

    if DRY_RUN:
        warning_log(f"dry-run: Would have copied {src} -> {dst}")
        return

    # Create the path to the dst file if it does not exist
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

    # What the heck is this?
    else:
        raise ValueError("Unsupported file: {}".format(src))

    # Set the good mode to the file or folder recursively
    chmod(dst)


def link(link_path: str, file_path: str) -> None:
    """
    Create a link to a target file or a folder.

    For the sake of simplicity, both target and link_to must be absolute path and must
    include the filename of the file or folder.
    Also do not include any trailing slash.

    e.g. link('/path/to/file', '/path/to/link')

    But not: link('/path/to/file', 'path/to/')
    or link('/path/to/folder/', '/path/to/link')

    Args:
        file_path (str): file or folder the link will point to
        link_path (str): Link to create
    """
    # skip this check in dry-run mode
    if not os.path.exists(file_path) and not DRY_RUN:
        error(f"Could not create link from {link_path} to {file_path}. {file_path} does not exist")

    assert isinstance(file_path, str)
    assert isinstance(link_path, str)

    if DRY_RUN:
        warning_log(f"dry-run: Would have created link at {link_path} to file {file_path}")
        return

    # Create the path to the link if it does not exist
    abs_path = os.path.dirname(os.path.abspath(link_path))
    if not os.path.isdir(abs_path):
        os.makedirs(abs_path)

    # Make sure the file or folder recursively has the good mode
    chmod(file_path)

    # Create the link to target
    # the 'src' in a symlink is the path to the LINK
    # the 'dest' is the real file
    # os.symlink(src, dest)
    os.symlink(link_path, file_path)


def delete_and_link(mackup_filepath: str, home_filepath: str) -> None:
    """
    Delete the original file and replace with symlink
    """
    # Delete the dest file if it exists
    if os.path.exists(home_filepath):
        delete(home_filepath)

    # Link the backed-up file to its original place
    link(home_filepath, mackup_filepath)


def backup(mackup_filepath: str, home_filepath: str):
    """ Create file in Mackup dir from original in home dir """
    if os.path.islink(home_filepath):
        warning_log(
            f"The file {os.path.basename(home_filepath)} is already a symlink.  Skipping copy to mackup directory")
        return

    # if the file exists, compare them
    if os.path.exists(mackup_filepath):
        files_are_equal, diff = compare_file_contents(mackup_filepath, home_filepath)
        if files_are_equal:
            vlog(f"Found identical file {os.path.basename(mackup_filepath)} in both home and mackup dirs.  Skipping")
            return
        else:
            warning_log(f"You already have a {get_file_type(mackup_filepath)} named {os.path.basename(mackup_filepath)} in your mackup directory.")
            if diff is not None:
                warning_log("Here is the diff:\n")
                warning_log(diff)
            if not confirm(f"Do you want to replace it with the original from your home directory?  This will overwrite {mackup_filepath}"):
                info_log(f"User declined to replace existing file {mackup_filepath}.  Skipping")
                return

    vlog(f"Copying {home_filepath} to {mackup_filepath}")
    copy(home_filepath, mackup_filepath)

    if not SHOULD_COPY:
        vlog(f"Deleting {home_filepath} and replacing with link to {mackup_filepath}")
        delete_and_link(mackup_filepath, home_filepath)


def restore(mackup_filepath: str, home_filepath: str):
    """
    Restore file from cloud storage to home dir
    :return:
    """

    # if the file exists, compare them
    if os.path.exists(home_filepath):
        files_are_equal, diff = compare_file_contents(mackup_filepath, home_filepath)
        if files_are_equal:
            vlog(f"Found identical file {os.path.basename(mackup_filepath)} in both home and mackup dirs.  Skipping")
            return
        else:
            warning_log(f"You already have a {get_file_type(home_filepath)} named {os.path.basename(home_filepath)} in your home directory.")
            if diff is not None:
                warning_log("Here is the diff:\n")
                warning_log(diff)
            if not confirm(f"Do you want to replace it with the original from your home directory?  This will overwrite {home_filepath}"):
                print(f"Not replacing existing file {home_filepath}.  Skipping")
                return

    vlog(f"Copying {mackup_filepath} to {home_filepath}")
    copy(mackup_filepath, home_filepath)

    if not SHOULD_COPY:
        vlog(f"Deleting {home_filepath} and replacing with link to {mackup_filepath}")
        delete_and_link(mackup_filepath, home_filepath)


def chmod(target: str) -> None:
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


def get_file_type(filename: str) -> str:
    # Name it right
    if os.path.isfile(filename):
        file_type = "file"
    elif os.path.isdir(filename):
        file_type = "folder"
    elif os.path.islink(filename):
        file_type = "link"
    else:
        raise ValueError("Unsupported file: {}".format(filename))
    return file_type


def error(message: str) -> None:
    """
    Throw an error with the given message and immediately quit.

    Args:
        message(str): The message to display.
    """
    sys.exit(red(f"ERROR: {message}"))


def get_dropbox_folder_location() -> str:
    """
    Try to locate the Dropbox folder.

    Returns:
        (str) Full path to the current Dropbox folder
    """
    host_db_path = os.path.join(os.environ["HOME"], ".dropbox/host.db")
    try:
        with open(host_db_path, "r") as f_hostdb:
            data = f_hostdb.read().split()
    except IOError:
        error(constants.ERROR_UNABLE_TO_FIND_STORAGE.format(provider="Dropbox install"))
    dropbox_home = base64.b64decode(data[1]).decode()

    return dropbox_home


def get_google_drive_folder_location() -> str:
    """
    Try to locate the Google Drive folder.

    Returns:
        (str) Full path to the current Google Drive folder
    """
    gdrive_db_path = "Library/Application Support/Google/Drive/sync_config.db"
    yosemite_gdrive_db_path = (
        "Library/Application Support/Google/Drive/" "user_default/sync_config.db"
    )
    yosemite_gdrive_db = os.path.join(os.environ["HOME"], yosemite_gdrive_db_path)
    if os.path.isfile(yosemite_gdrive_db):
        gdrive_db_path = yosemite_gdrive_db

    googledrive_home = None

    gdrive_db = os.path.join(os.environ["HOME"], gdrive_db_path)
    if os.path.isfile(gdrive_db):
        con = sqlite3.connect(gdrive_db)
        if con:
            cur = con.cursor()
            query = (
                "SELECT data_value "
                "FROM data "
                "WHERE entry_key = 'local_sync_root_path';"
            )
            cur.execute(query)
            data = cur.fetchone()
            googledrive_home = str(data[0])
            con.close()

    if not googledrive_home:
        error(
            constants.ERROR_UNABLE_TO_FIND_STORAGE.format(
                provider="Google Drive install"
            )
        )

    return googledrive_home


def get_copy_folder_location() -> str:
    """
    Try to locate the Copy folder.

    Returns:
        (str) Full path to the current Copy folder
    """
    copy_settings_path = "Library/Application Support/Copy Agent/config.db"
    copy_home = None

    copy_settings = os.path.join(os.environ["HOME"], copy_settings_path)

    if os.path.isfile(copy_settings):
        database = sqlite3.connect(copy_settings)
        if database:
            cur = database.cursor()
            query = "SELECT value " "FROM config2 " "WHERE option = 'csmRootPath';"
            cur.execute(query)
            data = cur.fetchone()
            copy_home = str(data[0])
            cur.close()

    if not copy_home:
        error(constants.ERROR_UNABLE_TO_FIND_STORAGE.format(provider="Copy install"))

    return copy_home


def get_icloud_folder_location() -> str:
    """
    Try to locate the iCloud Drive folder.

    Returns:
        (str) Full path to the iCloud Drive folder.
    """
    yosemite_icloud_path = "~/Library/Mobile Documents/com~apple~CloudDocs/"

    icloud_home = os.path.expanduser(yosemite_icloud_path)

    if not os.path.isdir(icloud_home):
        error(constants.ERROR_UNABLE_TO_FIND_STORAGE.format(provider="iCloud Drive"))

    return str(icloud_home)


def is_process_running(process_name: str) -> bool:
    """
    Check if a process with the given name is running.

    Args:
        (str): Process name, e.g. "Sublime Text"

    Returns:
        (bool): True if the process is running
    """
    is_running = False

    # On systems with pgrep, check if the given process is running
    if os.path.isfile("/usr/bin/pgrep"):
        dev_null = open(os.devnull, "wb")
        returncode = subprocess.call(["/usr/bin/pgrep", process_name], stdout=dev_null)
        is_running = bool(returncode == 0)

    return is_running


def remove_acl(path: str) -> None:
    """
    Remove the ACL of the file or folder located on the given path.

    Also remove the ACL of any file and folder below the given one,
    recursively.

    Args:
        path (str): Path to the file or folder to remove the ACL for,
                    recursively.
    """
    # Some files have ACLs, let's remove them recursively
    if platform.system() == constants.PLATFORM_DARWIN and os.path.isfile("/bin/chmod"):
        subprocess.call(["/bin/chmod", "-R", "-N", path])
    elif (platform.system() == constants.PLATFORM_LINUX) and os.path.isfile(
            "/bin/setfacl"
    ):
        subprocess.call(["/bin/setfacl", "-R", "-b", path])


def remove_immutable_attribute(path: str) -> None:
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
    if (platform.system() == constants.PLATFORM_DARWIN) and os.path.isfile(
            "/usr/bin/chflags"
    ):
        subprocess.call(["/usr/bin/chflags", "-R", "nouchg", path])
    elif platform.system() == constants.PLATFORM_LINUX and os.path.isfile(
            "/usr/bin/chattr"
    ):
        subprocess.call(["/usr/bin/chattr", "-R", "-f", "-i", path])


def can_file_be_synced_on_current_platform(path: str) -> None:
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
    fullpath = os.path.join(os.environ["HOME"], path)

    # Compute the ~/Library path on macOS
    # End it with a slash because we are looking for this specific folder and
    # not any file/folder named LibrarySomething
    library_path = os.path.join(os.environ["HOME"], "Library/")

    if platform.system() == constants.PLATFORM_LINUX:
        if fullpath.startswith(library_path):
            can_be_synced = False

    return can_be_synced


def is_synced_with_mackup(mackup_filepath: str, home_filepath: str) -> Tuple[bool, Optional[str]]:
    """
    Determine whether the file is pointing to mackup or not
    If SHOULD_COPY is True, ensure that the contents are equivalent and the files are not linked
    Otherwise, ensure it's a symlink
    """
    # we might end up with a diff
    diff = None
    if not os.path.exists(mackup_filepath) or not os.path.exists(home_filepath):
        pointing_to_mackup = False
    elif SHOULD_COPY:
        if os.path.islink(home_filepath):
            delete(home_filepath)
            pointing_to_mackup = False
        elif os.path.isdir(mackup_filepath) and os.path.isdir(home_filepath):
            pointing_to_mackup = compare_dirs(mackup_filepath, home_filepath)
        elif os.path.isfile(mackup_filepath) and os.path.isfile(home_filepath):
            pointing_to_mackup, diff = compare_file_contents(mackup_filepath, home_filepath)
        else:
            # This means we want to copy, we don't have an existing symlink, and we have either 1 file and 1 folder,
            # or one of them doesn't exist
            pointing_to_mackup = False
    else:
        pointing_to_mackup = (
                os.path.islink(home_filepath)
                and os.path.exists(mackup_filepath)
                and os.path.samefile(mackup_filepath, home_filepath)
        )

    return (pointing_to_mackup, diff)


def compare_dirs(dir1: str, dir2: str) -> bool:
    """
    Compares two directories
    """
    dirs_are_equal = True
    res = filecmp.dircmp(dir1, dir2)
    if len(res.diff_files) > 0:
        dirs_are_equal = False
        print(f"Found differences between {dir1} and {dir2}:")
        if VERBOSE:
            res.report_full_closure()
        else:
            res.report()
    return dirs_are_equal


def is_unicode_file(filename: str) -> bool:
    """ Detect whether a file is unicode or something else (likely a binary file) """
    try:
        with open(filename, "r") as f:
            f.readline()
            return True
    except UnicodeDecodeError:
        return False


def compare_file_contents(filename1: str, filename2: str) -> Tuple[bool, Optional[str]]:
    """
    Compare the contents of two files.  Ensure they are not symlinks
    """
    vlog(f"{os.path.basename(filename1)} exists in both mackup and home dirs.  Comparing file content")

    # Maximum file size we'll read into memory.  If it's bigger than this, don't bother
    file_read_max_size = 1048576


    # if they are plist files, we can compare them and generate a diff
    _, filename1_ext = os.path.splitext(filename1)
    if filename1_ext == ".plist":
        return compare_files_plist(filename1, filename2)

    # determine whether they are binary files or text files.  only handles unicode
    if not is_unicode_file(filename1) or not is_unicode_file(filename2):
        vlog("Determined that the files are not unicode files.  Comparing as binary files")
        return (compare_files_binary(filename1, filename2), None)

    # if they are unicode, scan line by line and compare them
    with open(filename1, "r") as f1, open(filename2, "r") as f2:
        if os.path.getsize(filename1) > file_read_max_size or os.path.getsize(filename2) > file_read_max_size:
            # Compare file sizes - if they are different, files are different.
            if os.path.getsize(filename1) != os.path.getsize(filename2):
                return (False, None)
            else:
                # Otherwise compare contents
                return (compare_files_binary(filename1, filename2), None)

        # If the files unicode encoded and are smaller than 1mb, generate a diff as well
        return generate_diff(f1.read(), f2.read(), filename1, filename2)


def compare_files_binary(filename1: str, filename2: str, chunk_size: int = 1024) -> bool:
    """
    Compare two files without loading them entirely into memory.

    :param filename1: str, path to the first file
    :param filename2: str, path to the second file
    :param chunk_size: int, size of chunks to read and compare at a time
    :return: bool, True if files are identical, False otherwise
    """
    try:
        # Open both files.
        with open(filename1, 'rb') as file1, open(filename2, 'rb') as file2:
            # Compare file sizes - if they are different, files are different.
            if os.path.getsize(filename1) != os.path.getsize(filename2):
                return False

            # Compare contents chunk by chunk.
            while chunk := file1.read(chunk_size):
                if chunk != file2.read(chunk_size):
                    return False
        return True
    except FileNotFoundError:
        return False


def compare_files_plist(filename1: str, filename2: str) -> Tuple[bool, Optional[str]]:
    # Load the plist files
    with open(filename1, 'rb') as f1, open(filename2, "rb") as f2:
        plist_data1 = plistlib.load(f1)
        plist_data2 = plistlib.load(f2)

        # Convert to pretty-printed json so we get better diffs
        plist_str1 = json.dumps(plist_data1, indent=2, default=lambda o: "<not serializable>")
        plist_str2 = json.dumps(plist_data2, indent=2, default=lambda o: "<not serializable>")

        # Generate diff
        return generate_diff(plist_str1, plist_str2, filename1, filename2)


def generate_diff(s1: str, s2: str, filename1: str, filename2: str) -> Tuple[bool, Optional[str]]:
    str_data1 = s1.splitlines()
    str_data2 = s2.splitlines()

    # Generate and print the diff
    diff = list(difflib.unified_diff(str_data1, str_data2, fromfile=filename1, tofile=filename2))

    if any(line.startswith(('-', '+', '?')) for line in diff):
        diff_str = re.sub("\n+", "\n", "\n".join(diff))
        return (False, diff_str)
    else:
        return (True, None)

