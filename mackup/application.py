"""
Application Profile.

An Application Profile contains all the information about an application in
Mackup. Name, files, ...
"""

import os

from . import utils
from .mackup import Mackup


class ApplicationProfile(object):
    """Instantiate this class with application specific data."""

    def __init__(self, mackup, files, dry_run, verbose):
        """
        Create an ApplicationProfile instance.

        Args:
            mackup (Mackup)
            files (list)
        """
        assert isinstance(mackup, Mackup)
        assert isinstance(files, set)

        self.mackup = mackup
        self.files = list(files)
        self.dry_run = dry_run
        self.verbose = verbose

    def getFilepaths(self, filename):
        """
        Get home and mackup filepaths for given file

        Args:
            filename (str)

        Returns:
            home_filepath, mackup_filepath (str, str)
        """
        return os.path.join(os.environ['HOME'], filename), os.path.join(self.mackup.mackup_folder, filename)

    def backup(self):
        """
        Backup the application config files.

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
            (home_filepath, mackup_filepath) = self.getFilepaths(filename)

            home_exists = os.path.exists(home_filepath)
            if home_exists:
                home_is_f = os.path.isfile(home_filepath)
                home_is_d = os.path.isdir(home_filepath)
                home_is_l = os.path.islink(home_filepath)
            else:
                home_is_f = home_is_d = home_is_l = False

            mack_exists = os.path.exists(mackup_filepath)
            if mack_exists:
                mack_is_f = os.path.isfile(mackup_filepath)
                mack_is_d = os.path.isdir(mackup_filepath)
                mack_is_l = os.path.islink(mackup_filepath)
                if home_is_f or home_is_d or home_is_l:
                    mack_same = os.path.samefile(home_filepath, mackup_filepath)
                else:
                    mack_same = False
            else:
                mack_is_f = mack_is_d = mack_is_l = mack_same = False

            # If the file exists and is not already a link pointing to Mackup
            if (home_is_f or home_is_d) and not (home_is_l and (mack_is_f or mack_is_d) and mack_same):
                if self.verbose:
                    print("Backing up {} to {} ...".format(home_filepath, mackup_filepath))
                else:
                    print("Backing up {} ...".format(filename))

                if self.dry_run:
                    continue

                # Check if we already have a backup
                if mack_exists:
                    # Name it right
                    if mack_is_l:
                        file_type = 'link'
                    elif mack_is_d:
                        file_type = 'folder'
                    elif mack_is_f:
                        file_type = 'file'
                    else:
                        raise ValueError("Unsupported file: {}".format(mackup_filepath))

                    # Ask the user if he really want to replace it
                    if utils.confirm("A {} named {} already exists in the backup.\n"
                                     "Are you sure that you want to replace it ?".format(file_type, mackup_filepath)):
                        # Delete the file in Mackup
                        utils.delete(mackup_filepath)
                        utils.link(home_filepath, mackup_filepath, physical=True)
                else:
                    utils.link(home_filepath, mackup_filepath, physical=True)
            elif self.verbose:
                if home_exists:
                    print("Doing nothing {} is already backed up to {}".format(home_filepath, mackup_filepath))
                elif home_is_l:
                    print("Doing nothing {} is a broken link, you might want to fix it.".format(home_filepath))
                else:
                    print("Doing nothing {} does not exist".format(home_filepath))

    def restore(self):
        """
        Restore the application config files.

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
            (home_filepath, mackup_filepath) = self.getFilepaths(filename)

            # If the file exists and is not already pointing to the mackup file
            # and the folder makes sense on the current platform (Don't sync
            # any subfolder of ~/Library on GNU/Linux)
            file_or_dir_exists = (os.path.isfile(mackup_filepath) or
                                  os.path.isdir(mackup_filepath))
            pointing_to_mackup = (os.path.islink(home_filepath) and
                                  os.path.exists(mackup_filepath) and
                                  os.path.samefile(mackup_filepath, home_filepath))
            supported = utils.can_file_be_synced_on_current_platform(filename)

            if file_or_dir_exists and not pointing_to_mackup and supported:
                if self.verbose:
                    print("Restoring\n  linking {}\n  to      {} ...".format(home_filepath, mackup_filepath))
                else:
                    print("Restoring {} ...".format(filename))

                if self.dry_run:
                    continue

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
                        raise ValueError("Unsupported file: {}".format(mackup_filepath))

                    if utils.confirm("You already have a {} named {} in your home.\n"
                                     "Do you want to replace it with your backup ?".format(file_type, filename)):
                        utils.delete(home_filepath)
                        utils.link(mackup_filepath, home_filepath, physical=True)
                else:
                    utils.link(mackup_filepath, home_filepath, physical=True)
            elif self.verbose:
                if os.path.exists(home_filepath):
                    print("Doing nothing\n  {}\n  already linked by\n  {}".format(mackup_filepath, home_filepath))
                elif os.path.islink(home_filepath):
                    print("Doing nothing\n  {}\n  is a broken link, you might want to fix it.".format(home_filepath))
                else:
                    print("Doing nothing\n  {}\n  does not exist".format(mackup_filepath))

    def uninstall(self):
        pass
