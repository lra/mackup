"""
Application Profile.

An Application Profile contains all the information about an application in
Mackup. Name, files, ...
"""
import os
import logging
import traceback

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from . import utils


class ApplicationProfile(object):
    """
    Represents an application profile (config file) and contains all the logic
    to backup and restore applications
    """

    def __init__(self, name):
        """
        Create an ApplicationProfile instance.

        Args:
            name The appliaction name as in the config's basename
        """
        self.name = name
        self.files = set()

    @staticmethod
    def get_from_file(config_file):
        """Instanciate an ApplicationProfile from a given file"""

        config = configparser.SafeConfigParser(allow_no_value=True)

        # Needed to not lowercase the configuration_files in the ini files
        config.optionxform = str

        logging.debug("Reading config from: %s" % config_file)
        config.read(config_file)

        # Start building a dict for this app
        tmp_app = ApplicationProfile(config.get('application', 'name'))

        # Add the configuration files to sync
        if config.has_section('configuration_files'):
            for path in config.options('configuration_files'):
                if path.startswith('/'):
                    raise ValueError('Unsupported absolute path: {}'
                                     .format(path))

                # TODO: Here add encryption option! (+path)
                tmp_app.files.add(path)

        # Add the XDG configuration files to sync
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config_home and config.has_section('xdg_configuration_files'):
            logging.debug("Config contains XDG Files")
            if not os.path.exists(xdg_config_home):
                raise ValueError('$XDG_CONFIG_HOME: {} does not exist'
                                 .format(xdg_config_home))

            home = os.path.expanduser('~/')
            if not xdg_config_home.startswith(home):
                raise ValueError('$XDG_CONFIG_HOME: {} must be '
                                 'somewhere within your home '
                                 'directory: {}'
                                 .format(xdg_config_home, home))

            for path in config.options('xdg_configuration_files'):
                if path.startswith('/'):
                    raise ValueError('Unsupported absolute path: '
                                     '{}'
                                     .format(path))

                tmp_app.files.add(
                    os.path.join(xdg_config_home, path).replace(home, '')
                )

        return tmp_app

    def backup(self, mackup):
        """Public API wrapper to decide the correct method based on the mode"""
        try:
            getattr(self, "_backup_%s" % mackup.config.mode)(mackup)
        except AttributeError as e:
            logging.debug(traceback.format_exc())
            utils.error("Not implemented mode '%s'" % mackup.config.mode)

    def _backup_copy(self, mackup):
        """
        Copy mode backup
        """
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = mackup.get_abs_file_path(
                filename
            )

            if not os.path.exists(home_filepath):
                if mackup.verbose:
                    print("Doing nothing\n  {}\n  does not exist"
                          .format(home_filepath))
                continue

            if mackup.verbose:
                print("Backing up\n  {}\n  to\n  {} ..."
                      .format(home_filepath, mackup_filepath))
            else:
                print("Backing up {} ...".format(filename))

            if mackup.dry_run:
                continue

            if os.path.islink(home_filepath):
                real_path = os.path.realpath(home_filepath)
                print("WARNING: %s is a link to %s" %
                      (home_filepath, real_path))
                print("         Copying it either way")

            # If normal file/dir, copy it
            utils.copy(home_filepath, mackup_filepath)

    def _backup_link(self, mackup):
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
            (home_filepath, mackup_filepath) = mackup.get_abs_file_path(
                filename
            )

            # If the file exists and is not already a link pointing to Mackup
            if ((os.path.isfile(home_filepath) or
                 os.path.isdir(home_filepath)) and
                not (os.path.islink(home_filepath) and
                     (os.path.isfile(mackup_filepath) or
                      os.path.isdir(mackup_filepath)) and
                     os.path.samefile(home_filepath,
                                      mackup_filepath))):

                if mackup.verbose:
                    print("Backing up\n  {}\n  to\n  {} ..."
                          .format(home_filepath, mackup_filepath))
                else:
                    print("Backing up {} ...".format(filename))

                if mackup.dry_run:
                    continue

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
                    if utils.confirm("A {} named {} already exists in the"
                                     " backup.\nAre you sure that you want to"
                                     " replace it ?"
                                     .format(file_type, mackup_filepath)):
                        # Delete the file in Mackup
                        utils.delete(mackup_filepath)
                        # Copy the file
                        utils.copy(home_filepath, mackup_filepath)
                        # Delete the file in the home
                        utils.delete(home_filepath)
                        # Link the backuped file to its original place
                        utils.link(mackup_filepath, home_filepath)
                else:
                    # Copy the file
                    utils.copy(home_filepath, mackup_filepath)
                    # Delete the file in the home
                    utils.delete(home_filepath)
                    # Link the backuped file to its original place
                    utils.link(mackup_filepath, home_filepath)
            elif mackup.verbose:
                if os.path.exists(home_filepath):
                    print("Doing nothing\n  {}\n  "
                          "is already backed up to\n  {}"
                          .format(home_filepath, mackup_filepath))
                elif os.path.islink(home_filepath):
                    print("Doing nothing\n  {}\n  "
                          "is a broken link, you might want to fix it."
                          .format(home_filepath))
                else:
                    print("Doing nothing\n  {}\n  does not exist"
                          .format(home_filepath))

    def restore(self, mackup):
        """Public API wrapper to decide the correct method based on the mode"""
        try:
            getattr(self, "_restore_%s" % mackup.config.mode)(mackup)
        except AttributeError as e:
            logging.debug(traceback.format_exc())
            utils.error("Not implemented mode '%s'" % mackup.config.mode)

    def _restore_copy(self, mackup):
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = mackup.get_abs_file_path(
                filename
            )

            if not os.path.exists(mackup_filepath):
                if mackup.verbose:
                    print("Doing nothing\n  {}\n  does not exist"
                          .format(mackup_filepath))
                continue

            if mackup.verbose:
                print("Restoring\n  {}\n  to\n  {} ..."
                      .format(home_filepath, mackup_filepath))
            else:
                print("Restoring {} ...".format(filename))

            if mackup.dry_run:
                continue

            file_type = utils.get_file_type(home_filepath)
            if utils.confirm(
                "You already have a {} named {} in your"
                " home.\nBackup   {}\nExisting {}\n"
                "Do you want to replace it with"
                " your backup ?".format(
                    file_type, filename,
                    utils.get_creation_time_str(mackup_filepath),
                    utils.get_creation_time_str(home_filepath))):

                utils.copy(mackup_filepath, home_filepath)

    def _restore_link(self, mackup):
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
            (home_filepath, mackup_filepath) = mackup.get_abs_file_path(
                filename
            )

            # If the file exists and is not already pointing to the mackup file
            # and the folder makes sense on the current platform (Don't sync
            # any subfolder of ~/Library on GNU/Linux)
            file_or_dir_exists = (os.path.isfile(mackup_filepath) or
                                  os.path.isdir(mackup_filepath))
            pointing_to_mackup = (os.path.islink(home_filepath) and
                                  os.path.exists(mackup_filepath) and
                                  os.path.samefile(mackup_filepath,
                                                   home_filepath))
            supported = utils.can_file_be_synced_on_current_platform(filename)

            # Check exit cases
            if not supported:
                continue

            if not file_or_dir_exists:
                if mackup.verbose:
                    print("Doing nothing\n  {}\n  does not exist"
                          .format(mackup_filepath))
                continue

            if pointing_to_mackup:
                if mackup.verbose:
                    if os.path.exists(home_filepath):
                        print("Doing nothing\n  {}\n  already linked by\n  {}"
                              .format(mackup_filepath, home_filepath))
                    elif os.path.islink(home_filepath):
                        print("Doing nothing\n  {}\n  "
                              "is a broken link, you might want to fix it."
                              .format(home_filepath))
                continue

            # Do the job here
            if mackup.verbose:
                print("Restoring\n  linking {}\n  to      {} ..."
                      .format(home_filepath, mackup_filepath))
            else:
                print("Restoring {} ...".format(filename))

            if mackup.dry_run:
                continue

            # Check if there is already a file in the home folder
            # If not link and return
            if not os.path.exists(home_filepath):
                utils.link(mackup_filepath, home_filepath)
                continue

            # Name it right
            file_type = utils.get_file_type(home_filepath)

            if utils.confirm("You already have a {} named {} in your"
                             " home.\nDo you want to replace it with"
                             " your backup ?"
                             .format(file_type, filename)):
                utils.delete(home_filepath)
                utils.link(mackup_filepath, home_filepath)

    def uninstall(self, mackup):
        """Public API wrapper to decide the correct method based on the mode"""
        try:
            getattr(self, "_uninstall_%s" % mackup.config.mode)(mackup)
        except AttributeError as e:
            logging.debug(traceback.format_exc())
            utils.error("Not implemented mode '%s'" % mackup.config.mode)

    def _uninstall_copy(self, mackup):
        """
        This doesnt do much... Mackup class handles this one.
        """
        pass

    def _uninstall_link(self, mackup):
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
            (home_filepath, mackup_filepath) = mackup.get_abs_file_path(
                filename
            )

            # If the mackup file exists
            if (not os.path.isfile(mackup_filepath) and
                    not os.path.isdir(mackup_filepath)):
                if mackup.verbose:
                    print("Doing nothing, {} does not exist"
                          .format(mackup_filepath))

                continue

            # Check if there is a corresponding file in the home folder
            if os.path.exists(home_filepath):
                if mackup.verbose:
                    print("Reverting {}\n  at {} ..."
                          .format(mackup_filepath, home_filepath))
                else:
                    print("Reverting {} ...".format(filename))

                if mackup.dry_run:
                    continue

                # If there is, delete it as we are gonna copy the Dropbox
                # one there
                utils.delete(home_filepath)

                # Copy the Dropbox file to the home folder
                utils.copy(mackup_filepath, home_filepath)
