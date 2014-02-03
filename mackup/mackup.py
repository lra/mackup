"""
The Mackup class is keeping all the state that mackup needs to keep during its
runtime. It also provides easy to use interface that is used by the Mackup UI.
The only UI for now is the command line.
"""
import os
import shutil
import tempfile
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from . import constants
from . import utils


class Mackup(object):
    """Main Mackup class"""

    def __init__(self):
        """Mackup Constructor"""
        try:
            self.dropbox_folder = utils.get_dropbox_folder_location()
        except IOError:
            utils.error(("Unable to find the Dropbox folder. If Dropbox is not"
                         " installed and running, go for it on"
                         " <http://www.dropbox.com/>"))

        self.mackup_folder = os.path.join(self.dropbox_folder,
                                          constants.MACKUP_BACKUP_PATH)
        self.temp_folder = tempfile.mkdtemp(prefix="mackup_tmp_")

    def _check_for_usable_environment(self):
        """Check if the current env is usable and has everything's required"""

        # Do we have a home folder ?
        if not os.path.isdir(self.dropbox_folder):
            utils.error(("Unable to find the Dropbox folder. If Dropbox is not"
                         " installed and running, go for it on"
                         " <http://www.dropbox.com/>"))

        # Do we have an old config file ?
        config = configparser.SafeConfigParser(allow_no_value=True)

        # Is the config file there ?
        path_to_cfg = "{}/{}".format(os.environ['HOME'],
                                     constants.MACKUP_CONFIG_FILE)
        if config.read(path_to_cfg):
            # Is an old setion is in the config file ?
            old_sections = ['Allowed Applications', 'Ignored Applications']
            for old_section in old_sections:
                if config.has_section(old_section):
                    utils.error(("Old config file detected. Aborting.\n"
                                 "\n"
                                 "An old section (e.g. [Allowed Applications]"
                                 " or [Ignored Applications] has been detected"
                                 " in your {} file.\n"
                                 "I'd rather do nothing than do something you"
                                 " do not want me to do.\n"
                                 "\n"
                                 "Please read the up to date documentation on"
                                 " <https://github.com/lra/mackup> and migrate"
                                 " your configuration file."
                                 .format(path_to_cfg)))

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
            utils.error("Unable to find the Mackup folder: {}\n"
                        "You might want to backup some files or get your"
                        " Dropbox folder synced first."
                        .format(self.mackup_folder))

    def clean_temp_folder(self):
        """Delete the temp folder and files created while running"""
        shutil.rmtree(self.temp_folder)

    def create_mackup_home(self):
        """If the Mackup home folder does not exist, create it"""
        if not os.path.isdir(self.mackup_folder):
            if utils.confirm("Mackup needs a folder to store your"
                             " configuration files\nDo you want to create it"
                             " now ? <{}>"
                             .format(self.mackup_folder)):
                os.mkdir(self.mackup_folder)
            else:
                utils.error("Mackup can't do anything without a home =(")
