"""
Keep your application settings in sync.

Copyright (C) 2013 Laurent Raufaste <http://glop.org/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

###########
# Imports #
###########


import argparse
import base64
import os
import platform
import shutil
import stat
import subprocess
import sys
import tempfile

# Py3k compatible
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


#############
# Constants #
#############


# Current version
VERSION = '0.6'

# Mode used to backup files to Dropbox
BACKUP_MODE = 'backup'

# Mode used to restore files from Dropbox
RESTORE_MODE = 'restore'

# Mode used to remove Mackup and reset and config file
UNINSTALL_MODE = 'uninstall'

# Support platforms
PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

# Directory containing the application configs
APPS_DIR = 'applications'

# Default Mackup backup path where it stores its files in Dropbox
MACKUP_BACKUP_PATH = 'Mackup'

# Mackup config file
MACKUP_CONFIG_FILE = '.mackup.cfg'
CUSTOM_APPS_DIR = '.mackup'


###########
# Classes #
###########


class ApplicationsDatabase(object):
    """Database containing all the configured applications"""

    def __init__(self):
        """
        Create a ApplicationsDatabase instance
        """
        # Configure the config parser
        apps_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                APPS_DIR)
        custom_apps_dir = os.path.join(os.environ['HOME'], CUSTOM_APPS_DIR)

        # Build the list of stock application config files
        config_files = []
        for filename in os.listdir(apps_dir):
            if filename.endswith('.cfg'):
                config_files.append(os.path.join(apps_dir, filename))

        # Append the list of custom application config files
        if os.path.isdir(custom_apps_dir):
            for filename in os.listdir(custom_apps_dir):
                if filename.endswith('.cfg'):
                    config_files.append(os.path.join(custom_apps_dir,
                                                     filename))

        # Build the dict that will contain the properties of each application
        self.apps = dict()

        for config_file in config_files:
            config = configparser.SafeConfigParser(allow_no_value=True)

            # Needed to not lowercase the configuration_files in the ini files
            config.optionxform = str

            if config.read(config_file):
                # Get the filename without the directory name
                filename = os.path.basename(config_file)
                # The app name is the cfg filename with the extension
                app_name = filename[:-len('.cfg')]

                # Start building a dict for this app
                self.apps[app_name] = dict()

                # Add the fancy name for the app, for display purpose
                app_pretty_name = config.get('application', 'name')
                self.apps[app_name]['name'] = app_pretty_name

                # Add the configuration files to sync
                self.apps[app_name]['configuration_files'] = set()
                if config.has_section('configuration_files'):
                    for cf in config.options('configuration_files'):
                        self.apps[app_name]['configuration_files'].add(cf)

    def get_name(self, name):
        """
        Return the fancy name of an application

        Args:
            name (str)

        Returns:
            str
        """
        return self.apps[name]['name']

    def get_files(self, name):
        """
        Return the list of config files of an application

        Args:
            name (str)

        Returns:
            list(str)
        """
        return list(self.apps[name]['configuration_files'])

    def get_app_names(self):
        """
        Return the list of application names that are available in the database

        Returns:
            list(str)
        """
        app_names = []
        for name in self.apps:
            app_names.append(name)

        return app_names

    def get_pretty_app_names(self):
        """
        Return the list of pretty app names that are available in the database

        Returns:
            list(str)
        """
        pretty_app_names = []
        for app_name in self.get_app_names():
            pretty_app_names.append(self.get_name(app_name))

        return pretty_app_names


class ApplicationProfile(object):
    """Instantiate this class with application specific data"""

    def __init__(self, mackup, files):
        """
        Create an ApplicationProfile instance

        Args:
            mackup (Mackup)
            files (list)
        """
        assert isinstance(mackup, Mackup)
        assert isinstance(files, list)

        self.mackup = mackup
        self.files = files

    def backup(self):
        """
        Backup the application config files

        Algorithm:
            if exists home/file
              if home/file is a real file
                if exists mackup/file
                  are you sure ?
                  if sure
                    rm mackup/file
                    mv home/file mackup/file
                    link mackup/file home/file
                else
                  mv home/file mackup/file
                  link mackup/file home/file
        """

        # For each file used by the application
        for filename in self.files:
            # Get the full path of each file
            filepath = os.path.join(os.environ['HOME'], filename)
            mackup_filepath = os.path.join(self.mackup.mackup_folder, filename)

            # If the file exists and is not already a link pointing to Mackup
            if ((os.path.isfile(filepath) or os.path.isdir(filepath))
                and not (os.path.islink(filepath)
                         and (os.path.isfile(mackup_filepath)
                              or os.path.isdir(mackup_filepath))
                         and os.path.samefile(filepath, mackup_filepath))):

                print "Backing up {}...".format(filename)

                # Check if we already have a backup
                if os.path.exists(mackup_filepath):

                    # Name it right
                    if os.path.isfile(mackup_filepath):
                        file_type = 'file'
                    elif os.path.isdir(mackup_filepath):
                        file_type = 'folder'
                    elif os.path.islink(mackup_filepath):
                        file_type = 'link'
                    else:
                        raise ValueError("Unsupported file: {}"
                                         .format(mackup_filepath))

                    # Ask the user if he really want to replace it
                    if confirm("A {} named {} already exists in the backup."
                               "\nAre you sure that your want to replace it ?"
                               .format(file_type, mackup_filepath)):
                        # Delete the file in Mackup
                        delete(mackup_filepath)
                        # Copy the file
                        copy(filepath, mackup_filepath)
                        # Delete the file in the home
                        delete(filepath)
                        # Link the backuped file to its original place
                        link(mackup_filepath, filepath)
                else:
                    # Copy the file
                    copy(filepath, mackup_filepath)
                    # Delete the file in the home
                    delete(filepath)
                    # Link the backuped file to its original place
                    link(mackup_filepath, filepath)

    def restore(self):
        """
        Restore the application config files

        Algorithm:
            if exists mackup/file
              if exists home/file
                are you sure ?
                if sure
                  rm home/file
                  link mackup/file home/file
              else
                link mackup/file home/file
        """

        # For each file used by the application
        for filename in self.files:
            # Get the full path of each file
            mackup_filepath = os.path.join(self.mackup.mackup_folder, filename)
            home_filepath = os.path.join(os.environ['HOME'], filename)

            # If the file exists and is not already pointing to the mackup file
            # and the folder makes sense on the current platform (Don't sync
            # any subfolder of ~/Library on GNU/Linux)
            if ((os.path.isfile(mackup_filepath)
                 or os.path.isdir(mackup_filepath))
                and not (os.path.islink(home_filepath)
                         and os.path.samefile(mackup_filepath,
                                              home_filepath))
                and can_file_be_synced_on_current_platform(filename)):

                print "Restoring {}...".format(filename)

                # Check if there is already a file in the home folder
                if os.path.exists(home_filepath):
                    # Name it right
                    if os.path.isfile(home_filepath):
                        file_type = 'file'
                    elif os.path.isdir(home_filepath):
                        file_type = 'folder'
                    elif os.path.islink(home_filepath):
                        file_type = 'link'
                    else:
                        raise ValueError("Unsupported file: {}"
                                         .format(mackup_filepath))

                    if confirm("You already have a {} named {} in your home.\n"
                               "Do you want to replace it with your backup ?"
                               .format(file_type, filename)):
                        delete(home_filepath)
                        link(mackup_filepath, home_filepath)
                else:
                    link(mackup_filepath, home_filepath)

    def uninstall(self):
        """
        Uninstall Mackup.
        Restore any file where it was before the 1st Mackup backup.

        Algorithm:
            for each file in config
                if mackup/file exists
                    if home/file exists
                        delete home/file
                    copy mackup/file home/file
            delete the mackup folder
            print how to delete mackup
        """
        # For each file used by the application
        for filename in self.files:
            # Get the full path of each file
            mackup_filepath = os.path.join(self.mackup.mackup_folder, filename)
            home_filepath = os.path.join(os.environ['HOME'], filename)

            # If the mackup file exists
            if (os.path.isfile(mackup_filepath)
                or os.path.isdir(mackup_filepath)):

                # Check if there is a corresponding file in the home folder
                if os.path.exists(home_filepath):
                    # If there is, delete it as we are gonna copy the Dropbox
                    # one there
                    delete(home_filepath)

                    # Copy the Dropbox file to the home folder
                    copy(mackup_filepath, home_filepath)


class Mackup(object):
    """Main Mackup class"""

    def __init__(self):
        """Mackup Constructor"""
        try:
            self.dropbox_folder = get_dropbox_folder_location()
        except IOError:
            error(("Unable to find the Dropbox folder."
                   " If Dropbox is not installed and running, go for it on"
                   " <http://www.dropbox.com/>"))

        self.mackup_folder = os.path.join(self.dropbox_folder,
                                          MACKUP_BACKUP_PATH)
        self.temp_folder = tempfile.mkdtemp(prefix="mackup_tmp_")

    def _check_for_usable_environment(self):
        """Check if the current env is usable and has everything's required"""

        # Do we have a home folder ?
        if not os.path.isdir(self.dropbox_folder):
            error(("Unable to find the Dropbox folder."
                   " If Dropbox is not installed and running, go for it on"
                   " <http://www.dropbox.com/>"))

        # Do we have an old config file ?
        config = configparser.SafeConfigParser(allow_no_value=True)

        # Is the config file there ?
        path_to_cfg = "{}/{}".format(os.environ['HOME'], MACKUP_CONFIG_FILE)
        if config.read(path_to_cfg):
            # Is an old setion is in the config file ?
            old_sections = ['Allowed Applications', 'Ignored Applications']
            for old_section in old_sections:
                if config.has_section(old_section):
                    error(("Old config file detected. Aborting.\n"
                           "\n"
                           "An old section (e.g. [Allowed Applications] or"
                           " [Ignored Applications] has been detected in your"
                           " {} file.\n"
                           "I'd rather do nothing than do something you do not"
                           " want me to do.\n"
                           "\n"
                           "Please read the up to date documentation on"
                           " <https://github.com/lra/mackup> and migrate your"
                           " configuration file.".format(path_to_cfg)))

        # Is Sublime Text running ?
        #if is_process_running('Sublime Text'):
        #    error(("Sublime Text is running. It is known to cause problems"
        #           " when Sublime Text is running while I backup or restore"
        #           " its configuration files. Please close Sublime Text and"
        #           " run me again."))

    def check_for_usable_backup_env(self):
        """Check if the current env can be used to back up files"""
        self._check_for_usable_environment()
        self.create_mackup_home()

    def check_for_usable_restore_env(self):
        """Check if the current env can be used to restore files"""
        self._check_for_usable_environment()

        if not os.path.isdir(self.mackup_folder):
            error("Unable to find the Mackup folder: {}\n"
                  "You might want to backup some files or get your Dropbox"
                  " folder synced first."
                  .format(self.mackup_folder))

    def clean_temp_folder(self):
        """Delete the temp folder and files created while running"""
        shutil.rmtree(self.temp_folder)

    def create_mackup_home(self):
        """If the Mackup home folder does not exist, create it"""
        if not os.path.isdir(self.mackup_folder):
            if confirm("Mackup needs a folder to store your configuration "
                       " files\nDo you want to create it now ? <{}>"
                       .format(self.mackup_folder)):
                os.mkdir(self.mackup_folder)
            else:
                error("Mackup can't do anything without a home =(")


####################
# Useful functions #
####################


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

    app_db = ApplicationsDatabase()

    # Format some epilog text
    epilog = "Supported applications:\n"
    for app_name in sorted(app_db.get_app_names()):
        epilog += " - {}\n".format(app_name)
    epilog += "\n\nMackup requires a fully synced Dropbox folder."

    # Setup the global parser
    parser = argparse.ArgumentParser(
        description=("Mackup {}\n"
                     "Keep your application settings in sync.\n"
                     "Copyright (C) 2013-2014 Laurent Raufaste"
                     " <http://glop.org/>\n"
                     .format(VERSION)),
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Add the required arg
    parser.add_argument("mode",
                        choices=[BACKUP_MODE, RESTORE_MODE, UNINSTALL_MODE],
                        help=("Backup will sync your conf files to Dropbox,"
                              " use this the 1st time you use Mackup.\n"
                              "Restore will link the conf files already in"
                              " Dropbox on your system, use it on any new"
                              " system you use.\n"
                              "Uninstall will reset everything as it was"
                              " before using Mackup."))

    # Parse the command line and return the parsed options
    return parser.parse_args()


def get_dropbox_folder_location():
    """
    Try to locate the Dropbox folder

    Returns:
        (str) Full path to the current Dropbox folder
    """
    host_db_path = os.environ['HOME'] + '/.dropbox/host.db'
    with open(host_db_path, 'r') as f:
        data = f.read().split()
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
    path_to_cfg = "{}/{}".format(os.environ['HOME'], MACKUP_CONFIG_FILE)
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
    app_db = ApplicationsDatabase()

    # If a config file exists, grab it and parser it
    config = configparser.SafeConfigParser(allow_no_value=True)

    # We allow all by default
    allowed_apps = app_db.get_app_names()

    # Is the config file there ?
    path_to_cfg = "{}/{}".format(os.environ['HOME'], MACKUP_CONFIG_FILE)
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
        DEVNULL = open(os.devnull, 'wb')
        returncode = subprocess.call(['/usr/bin/pgrep', process_name],
                                     stdout=DEVNULL)
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
    if platform.system() == PLATFORM_DARWIN and os.path.isfile('/bin/chmod'):
        subprocess.call(['/bin/chmod', '-R', '-N', path])
    elif ((platform.system() == PLATFORM_LINUX)
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
    if ((platform.system() == PLATFORM_DARWIN)
        and os.path.isfile('/usr/bin/chflags')):
        subprocess.call(['/usr/bin/chflags', '-R', 'nouchg', path])
    elif (platform.system() == PLATFORM_LINUX
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

    if platform.system() == PLATFORM_LINUX:
        if fullpath.startswith(library_path):
            can_be_synced = False

    return can_be_synced


################
# Main Program #
################


def main():
    """Main function"""

    # Get the command line arg
    args = parse_cmdline_args()

    mackup = Mackup()
    app_db = ApplicationsDatabase()

    if args.mode == BACKUP_MODE:
        # Check the env where the command is being run
        mackup.check_for_usable_backup_env()

        # Backup each application
        for app_name in get_apps_to_backup():
            app = ApplicationProfile(mackup, app_db.get_files(app_name))
            app.backup()

    elif args.mode == RESTORE_MODE:
        # Check the env where the command is being run
        mackup.check_for_usable_restore_env()

        for app_name in app_db.get_app_names():
            app = ApplicationProfile(mackup, app_db.get_files(app_name))
            app.restore()

    elif args.mode == UNINSTALL_MODE:
        # Check the env where the command is being run
        mackup.check_for_usable_restore_env()

        if confirm("You are going to uninstall Mackup.\n"
                   "Every configuration file, setting and dotfile managed"
                   " by Mackup will be unlinked and moved back to their"
                   " original place, in your home folder.\n"
                   "Are you sure ?"):
            for app_name in app_db.get_app_names():
                app = ApplicationProfile(mackup, app_db.get_files(app_name))
                app.uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mackup.mackup_folder)

            print ("\n"
                   "All your files have been put back into place. You can now"
                   " safely uninstall Mackup.\n"
                   "\n"
                   "Thanks for using Mackup !"
                   .format(os.path.abspath(__file__)))
    else:
        raise ValueError("Unsupported mode: {}".format(args.mode))

    # Delete the tmp folder
    mackup.clean_temp_folder()
