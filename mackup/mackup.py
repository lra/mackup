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
import logging

from . import utils
from . import config
from . import appsdb
from .constants import *
from .application import ApplicationProfile


class Mackup(object):
    """
    Main Mackup class.

    Use this as a container for the current environment, configuraion options
    and runtime options. This should idealy provide the complete mackup API.
    It also interfaces between the main code, the ApplicationsDatabase and the
    individual ApplicationProfiles
    """

    def __init__(self):
        """Mackup Constructor."""
        # Config
        self.config = config.Config()

        # Instantiate the app db
        self.app_db = appsdb.ApplicationsDatabase()

        # Default runtime options
        self.dry_run = False
        self.verbose = False

        self.mackup_folder = self.config.fullpath
        self.temp_folder = tempfile.mkdtemp(prefix="mackup_tmp_")

    def check_environment(self):
        """Check if the current env is usable and has everything's required."""
        # Do not let the user run Mackup as root
        if os.geteuid() == 0:
            utils.error("Running Mackup as a superuser is useless and"
                        " dangerous. Don't do it!")

        # Do we have a folder to put the Mackup folder ?
        if not os.path.isdir(self.config.path):
            utils.error("Unable to find the storage folder: {}"
                        .format(self.config.path))

    def check_backup_env(self):
        """Check if the current env can be used to back up files."""
        self.check_environment()
        self.create_mackup_home()

    def check_restore_env(self):
        """Check if the current env can be used to restore files."""
        self.check_environment()

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
        if os.path.isdir(self.mackup_folder):
            return

        if not utils.confirm("Mackup needs a directory to store your"
                         " configuration files\n"
                         "Do you want to create it now? <{}>"
                         .format(self.mackup_folder)):
            utils.error("Mackup can't do anything without a home =(")
            return

        # Create it here...
        os.makedirs(self.mackup_folder)

    def get_apps_to_backup(self):
        """
        Get the list of applications that should be backed up by Mackup.

        It's the list of allowed apps minus the list of ignored apps.

        Returns:
            (set) List of application names to back up
        """
        # If a list of apps to sync is specify, we only allow those
        # Or we allow every supported app by default
        apps_to_backup = self.config.apps_to_sync or self.app_db.get_app_names()

        # Remove the specified apps to ignore
        for app_name in self.config.apps_to_ignore:
            apps_to_backup.discard(app_name)

        return apps_to_backup

    def get_abs_file_path(self, filename):
        """
        Get home and mackup filepaths for given relative file path

        Args:
            filepath (str)

        Returns:
            home_filepath, mackup_filepath (str, str)
        """
        return (os.path.join(os.environ['HOME'], filename),
                os.path.join(self.mackup_folder, filename))

    def print_app_header(self, app_name):
        """
        Helper to print the application header if in verbose mode
        """
        if self.verbose:
            print(("\n{0} {1} {0}").format(header("---"), bold(app_name)))

    def backup(self):
        """
        Backup command implementation
        """
        logging.info("Backing up everything")

        # Check the env where the command is being run
        self.check_backup_env()

        # Backup each application
        for app_name in sorted(self.get_apps_to_backup()):
            self.print_app_header(app_name)
            self.app_db.apps[app_name].backup(self)

    def restore(self):
        # Check the env where the command is being run
        self.check_restore_env()

        # Restore the Mackup config before any other config, as we might need
        # it to know about custom settings
        mackup_app = ApplicationProfile(
            self.app_db.get_files(MACKUP_APP_NAME)
        )

        self.print_app_header(MACKUP_APP_NAME)
        mackup_app.restore(self)

        # Initialize again the apps db, as the Mackup config might have changed
        # it
        mckp = Mackup()
        app_db.load()

        # Restore the rest of the app configs, using the restored Mackup config
        app_names = mckp.get_apps_to_backup()
        # Mackup has already been done
        app_names.discard(MACKUP_APP_NAME)

        for app_name in sorted(self.get_apps_to_backup()):
            self.print_app_header(app_name)
            self.app_db.apps[app_name].restore(self)


    def uninstall(self):
        # Check the env where the command is being run
        self.check_restore_env()

        if self.dry_run or (
           utils.confirm("You are going to uninstall Mackup.\n"
                         "Every configuration file, setting and dotfile"
                         " managed by Mackup will be unlinked and moved back"
                         " to their original place, in your home folder.\n"
                         "Are you sure ?")):

            # Uninstall the apps except Mackup, which we'll uninstall last, to
            # keep the settings as long as possible
            app_names = self.get_apps_to_backup()
            app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(self.get_apps_to_backup()):
                self.print_app_header(app_name)
                self.app_db.apps[app_name].uninstall(self)

            # Uninstall the Mackup config last, as we might
            # need it to know about custom settings
            mackup_app = ApplicationProfile(
                self.app_db.get_files(MACKUP_APP_NAME)
            )

            self.print_app_header(MACKUP_APP_NAME)
            mackup_app.uninstall(self)

            # Delete the Mackup folder in Dropbox
            # NOTE: Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            print("\n"
                  "All your files have been put back into place. You can now"
                  " safely uninstall Mackup.\n"
                  "\n"
                  "Thanks for using Mackup!")

    def list(self):
        # Display the list of supported applications
        self.check_environment()
        app_names = self.app_db.get_app_names()

        output = "Supported applications:\n"
        for app_name in sorted(app_names):
          output += " - {}\n".format(app_name)
        output += "\n"
        output += ("{} applications supported in Mackup v{}"
                 .format(len(app_names), VERSION))
        print(output)
