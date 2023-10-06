"""
Application Profile.

An Application Profile contains all the information about an application in
Mackup. Name, files, ...
"""
import os
import platform
import textwrap
from typing import Set

from .mackup import Mackup
from . import utils
from .colors import cyan, info_log, warning_log


class ApplicationProfile(object):
    """Instantiate this class with application specific data."""

    def __init__(self, name: str, mackup: Mackup, files: Set[str]):
        """
        Create an ApplicationProfile instance.

        Args:
            mackup (Mackup)
            files (list)
        """
        assert isinstance(mackup, Mackup)
        assert isinstance(files, set)

        self.name = name
        self.mackup = mackup
        self.files = list(files)

    def getFilepaths(self, filename):
        """
        Get home and mackup filepaths for given file

        Args:
            filename (str)

        Returns:
            home_filepath, mackup_filepath (str, str)
        """
        return (
            os.path.join(os.environ["HOME"], filename),
            os.path.join(self.mackup.mackup_folder, filename),
        )

    def backup(self):
        """
        Backup the application config files.

        Algorithm:
            if exists home/file
              if home/file is a real file
                if exists mackup/file
                  are you sure?
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
            (home_filepath, mackup_filepath) = self.getFilepaths(filename)

            # If the config file doesn't exist, skip it
            if not os.path.exists(home_filepath):
                utils.vlog(f"Config file {filename} doesn't exist.  Skipping")
                continue

            # If it's a symlink already skip it
            if os.path.islink(home_filepath):
                warning_log(f"{filename} in home directory is a symlink.  Skipping")
                continue

            # Check whether the file is already synced with mackup
            is_synced_with_mackup, diff = utils.is_synced_with_mackup(mackup_filepath, home_filepath)
            if not is_synced_with_mackup:
                info_log(f"Backing up {filename}")
                utils.vlog(f"Syncing {home_filepath} to {mackup_filepath}")
                utils.backup(mackup_filepath, home_filepath)
            else:
                utils.vlog(f"{filename} is already synced")

    def restore(self):
        """
        Restore the application config files.

        Algorithm:
            if exists mackup/file
              if exists home/file
                are you sure?
                if sure
                  rm home/file
                  link mackup/file home/file
              else
                link mackup/file home/file
        """
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.getFilepaths(filename)

            # If the file exists and is not already pointing to the mackup file
            # and the folder makes sense on the current platform (Don't sync
            # any subfolder of ~/Library on GNU/Linux)
            mackup_file_exists = os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath)
            synced_with_mackup, diff = utils.is_synced_with_mackup(mackup_filepath, home_filepath)
            supported = utils.can_file_be_synced_on_current_platform(filename)

            if not supported:
                utils.vlog(f"File {filename} is not supported on platform {platform.system()}.  Skipping")
                continue

            if not mackup_file_exists:
                utils.vlog(f"{mackup_filepath} does not exist.  Skipping")
                continue

            if not synced_with_mackup:
                info_log(f"Restoring {mackup_filepath} to {home_filepath}")
                utils.restore(mackup_filepath, home_filepath)
            elif os.path.islink(home_filepath):
                warning_log(f"{home_filepath} is a broken link. Fixing")
                utils.delete(home_filepath)
                utils.restore(mackup_filepath, home_filepath)
            else:
                if os.path.exists(home_filepath):


                    utils.vlog(f"Doing nothing. {home_filepath} is already synced to {mackup_filepath}")

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
            (home_filepath, mackup_filepath) = self.getFilepaths(filename)

            # If the mackup file exists
            if os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath):
                # Check if there is a corresponding file in the home folder
                if os.path.exists(home_filepath):
                    print(f"Reverting {home_filepath} to {mackup_filepath}")
                    # If there is, delete it as we are gonna copy the Mackup file back into place
                    utils.delete(home_filepath)

                # Copy the Mackup file to the home folder
                utils.copy(mackup_filepath, home_filepath)
                utils.delete(mackup_filepath)
            else:
                utils.vlog(f"Doing nothing. {mackup_filepath} does not exist")
