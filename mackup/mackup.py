"""
The Mackup Class.

The Mackup class is keeping all the state that Mackup needs to keep during its
runtime. It also provides easy to use interface that is used by the Mackup UI.
The only UI for now is the command line.
"""
import os
import os.path
import shutil
import tempfile
import sys
import platform

from ctypes import Structure, windll, c_ulong, c_ulonglong, c_void_p, byref
from . import utils
from . import config
from . import appsdb
from . import constants


class Mackup(object):

    """Main Mackup class."""

    def __init__(self):
        """Mackup Constructor."""
        self._config = config.Config()

        self.mackup_folder = self._config.fullpath
        self.temp_folder = tempfile.mkdtemp(prefix="mackup_tmp_")

    def is_link_privilege_enabled(self):
        """Check if symbolic link creation privilege is enabled."""
        TOKEN_ALL_ACCESS = c_ulong(0x000f01ff)
        SE_CREATE_SYMBOLIC_LINK_NAME = 'SeCreateSymbolicLinkPrivilege'

        class LUID_AND_ATTRIBUTES(Structure):
            _fields_ = [
                ("Luid", c_ulonglong),
                ("Attributes", c_ulong)]

        class PRIVILEGE_SET(Structure):
            _fields_ = [
                ("PrivilegeCount", c_ulong),
                ("Control", c_ulong),
                ("Privilege", LUID_AND_ATTRIBUTES)]

        try:
            token = c_void_p(None)
            ret = windll.advapi32.OpenProcessToken(
                windll.kernel32.GetCurrentProcess(),
                TOKEN_ALL_ACCESS,
                byref(token))
            if ret == 0:
                return False

            luid = c_ulonglong(0)
            ret = windll.advapi32.LookupPrivilegeValueW(
                None, SE_CREATE_SYMBOLIC_LINK_NAME, byref(luid))
            if ret == 0:
                return False

            enabled = c_ulong(0)
            priv_set = PRIVILEGE_SET(1, 1, LUID_AND_ATTRIBUTES(luid, 2))
            ret = windll.advapi32.PrivilegeCheck(
                token, byref(priv_set), byref(enabled))
            return ret != 0 and enabled.value > 0

        except OSError:
            return False

    def check_link_support_on_windows(self):
        """Check if symbolic links can be created on Windows."""
        # Symbolic link support was introduced in Windows 6.0
        if sys.getwindowsversion()[0] < 6:
            utils.error("Mackup can only run on Windows 6.0 (Vista)"
                        " or higher.")

        # Added support for Windows symbolic links in version 3.2
        if sys.version_info[0] < 3 or sys.version_info[1] < 2:
            utils.error("Mackup need Python version 3.2 or highter.")

        if not self.is_link_privilege_enabled():
            utils.error("Mackup can not work without the"
                        " SeCreateSymbolicLinkPrivilege.\n"
                        "To grant this privilege, you have two choices:\n"
                        " 1. Log in with an administrator account and"
                        " launch mackup within a command\n"
                        "    prompt running as administrator.\n"
                        " 2. Use a standard account, and assign the"
                        " SeCreateSymbolicLinkPrivilege to\n"
                        "    your user or group via the local group policy"
                        " editor.")

    def check_for_usable_environment(self):
        """Check if the current env is usable and has everything's required."""

        if platform.system() == constants.PLATFORM_WINDOWS:
            # Symbolic link support is silly on Windows, so check it first.
            self.check_link_support_on_windows()
        else:
            # Do not let the user run Mackup as root
            if os.geteuid() == 0:
                utils.error("Running Mackup as a superuser is useless and"
                            " dangerous. Don't do it!")

        # Do we have a folder to put the Mackup folder ?
        if not os.path.isdir(self._config.path):
            utils.error("Unable to find the storage folder: {}"
                        .format(self._config.path))

        # Is Sublime Text running ?
        # if is_process_running('Sublime Text'):
        #    error("Sublime Text is running. It is known to cause problems"
        #          " when Sublime Text is running while I backup or restore"
        #          " its configuration files. Please close Sublime Text and"
        #          " run me again.")

    def check_for_usable_backup_env(self):
        """Check if the current env can be used to back up files."""
        self.check_for_usable_environment()
        self.create_mackup_home()

    def check_for_usable_restore_env(self):
        """Check if the current env can be used to restore files."""
        self.check_for_usable_environment()

        if not os.path.isdir(self.mackup_folder):
            utils.error("Unable to find the Mackup folder: {}\n"
                        "You might want to back up some files or get your"
                        " storage directory synced first."
                        .format(self.mackup_folder))

    def clean_temp_folder(self):
        """Delete the temp folder and files created while running."""
        shutil.rmtree(self.temp_folder)

    def create_mackup_home(self):
        """If the Mackup home folder does not exist, create it."""
        if not os.path.isdir(self.mackup_folder):
            if utils.confirm("Mackup needs a directory to store your"
                             " configuration files\n"
                             "Do you want to create it now? <{}>"
                             .format(self.mackup_folder)):
                os.makedirs(self.mackup_folder)
            else:
                utils.error("Mackup can't do anything without a home =(")

    def get_apps_to_backup(self):
        """
        Get the list of applications that should be backed up by Mackup.

        It's the list of allowed apps minus the list of ignored apps.

        Returns:
            (set) List of application names to back up
        """
        # Instantiate the app db
        app_db = appsdb.ApplicationsDatabase()

        # If a list of apps to sync is specify, we only allow those
        # Or we allow every supported app by default
        apps_to_backup = self._config.apps_to_sync or app_db.get_app_names()

        # Remove the specified apps to ignore
        for app_name in self._config.apps_to_ignore:
            apps_to_backup.discard(app_name)

        return apps_to_backup
