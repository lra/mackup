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
from typing import Optional

from . import appsdb, config, utils


class Mackup:
    """Main Mackup class."""

    def __init__(self, config_file: Optional[str] = None) -> None:
        """Mackup Constructor."""
        self._config: config.Config = config.Config(config_file)

        self.mackup_folder: str = self._config.fullpath
        self.temp_folder: str = tempfile.mkdtemp(prefix="mackup_tmp_")

    def check_for_usable_environment(self) -> None:
        """Check if the current env is usable and has everything's required."""

        # Allow only explicit superuser usage
        if os.geteuid() == 0 and not utils.CAN_RUN_AS_ROOT:
            utils.error(
                "Running Mackup as superuser can be dangerous."
                " Don't do it unless you know what you're doing!"
                " Run mackup --help for guidance.",
            )

        # Do we have a folder set to save Mackup content into?
        if not os.path.isdir(self._config.path):
            utils.error(
                f"Unable to find the storage folder: {self._config.path}",
            )

        # Is Sublime Text running?
        # if is_process_running('Sublime Text'):
        #    error("Sublime Text is running. It is known to cause problems"
        #          " when Sublime Text is running while I backup or restore"
        #          " its configuration files. Please close Sublime Text and"
        #          " run me again.")

    def check_for_usable_backup_env(self) -> None:
        """Check if the current env can be used to back up files."""
        self.check_for_usable_environment()
        self.create_mackup_home()

    def check_for_usable_restore_env(self) -> None:
        """Check if the current env can be used to restore files."""
        self.check_for_usable_environment()

        if not os.path.isdir(self.mackup_folder):
            utils.error(
                f"Unable to find the Mackup folder: {self.mackup_folder}\n"
                "You might want to back up some files or get your"
                " storage directory synced first.",
            )

    def clean_temp_folder(self) -> None:
        """Delete the temp folder and files created while running."""
        shutil.rmtree(self.temp_folder)

    def create_mackup_home(self) -> None:
        """If the Mackup home folder does not exist, create it."""
        if not os.path.isdir(self.mackup_folder):
            if utils.confirm(
                "Mackup needs a directory to store your"
                " configuration files\n"
                f"Do you want to create it now? <{self.mackup_folder}>",
            ):
                os.makedirs(self.mackup_folder)
            else:
                utils.error("Mackup can't do anything without a home =(")

    def get_apps_to_backup(self) -> set[str]:
        """
        Get the list of applications that should be backed up by Mackup.

        It's the list of allowed apps minus the list of ignored apps.

        Returns:
            (set) List of application names to back up
        """
        # Instantiate the app db
        app_db: appsdb.ApplicationsDatabase = appsdb.ApplicationsDatabase()

        # If a list of apps to sync is specify, we only allow those
        # Or we allow every supported app by default
        apps_to_backup: set[str] = self._config.apps_to_sync or app_db.get_app_names()

        # Remove the specified apps to ignore
        for app_name in self._config.apps_to_ignore:
            apps_to_backup.discard(app_name)

        return apps_to_backup
