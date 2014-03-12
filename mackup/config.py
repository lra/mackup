"""Package used to manage the .mackup.cfg config file."""

import os
import os.path
import sys

from .constants import (MACKUP_BACKUP_PATH,
                        MACKUP_CONFIG_FILE,
                        ENGINE_DROPBOX,
                        ENGINE_GDRIVE,
                        ENGINE_COPY,
                        ENGINE_ICLOUD,
                        ENGINE_BOX,
                        ENGINE_FS)

from .utils import (error,
                    get_dropbox_folder_location,
                    get_copy_folder_location,
                    get_google_drive_folder_location,
                    get_icloud_folder_location,
                    get_box_folder_location)
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def make_config_file(storage_type=ENGINE_DROPBOX, path="",
                     directory=MACKUP_BACKUP_PATH, whitelist=None,
                     blacklist=None):
    """
    Writes a configuration file (~/.mackup.cfg) using the parameters. If no
    options are specified, a default configuration file is made.

    Args:
        (str): The storage_type to be written (dropbox, google_drive,
        file_system)
        (str): The path to use if storage_type was file_system
        (str): The custom directory name that will be used
        (list): The list of applications that will be synced
        (list): The list of applications that will not be synced
    """
    # Get the names of the apps to check the whitelist and blacklist
    if not whitelist:
        whitelist = []
    if not blacklist:
        blacklist = []
    # Make sure the storage_type is correct
    assert storage_type in (ENGINE_DROPBOX, ENGINE_FS,
                            ENGINE_GDRIVE)
    # If the path is specified, make sure it exists
    if path:
        assert os.path.exists(path), (
            "The path {} does not exist!".format(path))
    # Write the configuration file in the home directory
    configuration = ["[storage]",
                     "engine = {}".format(storage_type),
                     ("path = " + (path or "")) if storage_type else "",
                     "directory = {}".format(directory),

                     "[applications_to_sync]",
                     "\n".join(whitelist),

                     "[applications_to_ignore]",
                     "\n".join(blacklist)
                     ]
    config_path = os.path.join(os.environ['HOME'],
                               MACKUP_CONFIG_FILE)
    with open(config_path, "w") as config_file:
        config_file.writelines(line + "\n" for line in configuration)


class Config(object):

    """The Mackup Config class."""

    def __init__(self, filename=None):
        """
        Create a Config instance.

        Args:
            filename (str): Optional filename of the config file. If empty,
                            defaults to MACKUP_CONFIG_FILE
        """
        assert isinstance(filename, str) or filename is None

        # Initialize the parser
        self._parser = self._setup_parser(filename)

        # Do we have an old config file ?
        self._warn_on_old_config()

        # Get the storage engine
        self._engine = self._parse_engine()

        # Get the path where the Mackup folder is
        self._path = self._parse_path()

        # Get the directory replacing 'Mackup', if any
        self._directory = self._parse_directory()

        # Get the list of apps to ignore
        self._apps_to_ignore = self._parse_apps_to_ignore()

        # Get the list of apps to allow
        self._apps_to_sync = self._parse_apps_to_sync()

    @property
    def engine(self):
        """
        The engine used by the storage.

        ENGINE_DROPBOX, ENGINE_GDRIVE, ENGINE_COPY, ENGINE_ICLOUD, ENGINE_BOX
        or ENGINE_FS.

        Returns:
            str
        """
        return str(self._engine)

    @property
    def path(self):
        """
        Path to the Mackup configuration files.

        The path to the directory where Mackup is gonna create and store his
        directory.

        Returns:
            str
        """
        return str(self._path)

    @property
    def directory(self):
        """
        The name of the Mackup directory, named Mackup by default.

        Returns:
            str
        """
        return str(self._directory)

    @property
    def fullpath(self):
        """
        Full path to the Mackup configuration files.

        The full path to the directory when Mackup is storing the configuration
        files.

        Returns:
            str
        """
        return str(os.path.join(self.path, self.directory))

    @property
    def apps_to_ignore(self):
        """
        Get the list of applications ignored in the config file.

        Returns:
            set. Set of application names to ignore, lowercase
        """
        return set(self._apps_to_ignore)

    @property
    def apps_to_sync(self):
        """
        Get the list of applications allowed in the config file.

        Returns:
            set. Set of application names to allow, lowercase
        """
        return set(self._apps_to_sync)

    def _setup_parser(self, filename=None):
        """
        Configure the ConfigParser instance the way we want it.

        Args:
            filename (str) or None

        Returns:
            SafeConfigParser
        """
        assert isinstance(filename, str) or filename is None

        # If we are not overriding the config filename
        if not filename:
            filename = MACKUP_CONFIG_FILE

        parser = configparser.SafeConfigParser(allow_no_value=True)
        parser.read(os.path.join(os.path.join(os.environ['HOME'], filename)))

        return parser

    def _warn_on_old_config(self):
        """Warn the user if an old config format is detected."""
        # Is an old setion is in the config file ?
        old_sections = ['Allowed Applications', 'Ignored Applications']
        for old_section in old_sections:
            if self._parser.has_section(old_section):
                error("Old config file detected. Aborting.\n"
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
                      .format(MACKUP_CONFIG_FILE))

    def _parse_engine(self):
        """
        Parse the storage engine in the config.

        Returns:
            str
        """
        if self._parser.has_option('storage', 'engine'):
            engine = str(self._parser.get('storage', 'engine'))
        else:
            engine = ENGINE_DROPBOX

        assert isinstance(engine, str)

        if engine not in [ENGINE_DROPBOX,
                          ENGINE_GDRIVE,
                          ENGINE_COPY,
                          ENGINE_ICLOUD,
                          ENGINE_BOX,
                          ENGINE_FS]:
            raise ConfigError('Unknown storage engine: {}'.format(engine))

        return str(engine)

    def _parse_path(self):
        """
        Parse the storage path in the config.

        Returns:
            str
        """
        if self.engine == ENGINE_DROPBOX:
            path = get_dropbox_folder_location()
        elif self.engine == ENGINE_GDRIVE:
            path = get_google_drive_folder_location()
        elif self.engine == ENGINE_COPY:
            path = get_copy_folder_location()
        elif self.engine == ENGINE_ICLOUD:
            path = get_icloud_folder_location()
        elif self.engine == ENGINE_BOX:
            path = get_box_folder_location()
        elif self.engine == ENGINE_FS:
            if self._parser.has_option('storage', 'path'):
                cfg_path = self._parser.get('storage', 'path')
                path = os.path.join(os.environ['HOME'], cfg_path)
            else:
                raise ConfigError("The required 'path' can't be found while"
                                  " the 'file_system' engine is used.")

        # Python 2 and python 3 byte strings are different.
        if sys.version_info[0] < 3:
            path = str(path)
        else:
            path = path.decode("utf-8")

        return path

    def _parse_directory(self):
        """
        Parse the storage directory in the config.

        Returns:
            str
        """
        if self._parser.has_option('storage', 'directory'):
            directory = self._parser.get('storage', 'directory')
        else:
            directory = MACKUP_BACKUP_PATH

        return str(directory)

    def _parse_apps_to_ignore(self):
        """
        Parse the applications to ignore in the config.

        Returns:
            set
        """
        # We ignore nothing by default
        apps_to_ignore = set()

        # Is the "[applications_to_ignore]" in the cfg file ?
        section_title = 'applications_to_ignore'
        if self._parser.has_section(section_title):
            apps_to_ignore = set(self._parser.options(section_title))

        return apps_to_ignore

    def _parse_apps_to_sync(self):
        """
        Parse the applications to backup in the config.

        Returns:
            set
        """
        # We allow nothing by default
        apps_to_sync = set()

        # Is the "[applications_to_sync]" section in the cfg file ?
        section_title = 'applications_to_sync'
        if self._parser.has_section(section_title):
            apps_to_sync = set(self._parser.options(section_title))

        return apps_to_sync

    @staticmethod
    def make_config_file():
        storage_type = choose("What method would you like to use to backup "
                              "your configuration files?",
                              ["dropbox", "google_drive", "file_system"])[0]
        path = ""
        if storage_type == "file_system":
            path = raw_input("Please enter the path where Mackup will save "
                              "your configuration files. You can use relative "
                              "or absolute paths\n")

        directory = "Mackup"
        if confirm("Would you like to customize the directory in which "
                         "Mackup stores your files?"):
            directory = raw_input("Directory name: ")

        whitelist = ""
        if not confirm("Would you like to sync all applications or "
                              "specify from a list of supported software?"):
            whitelist = choose("Choose any of the follwing "
            "deliminated by a space): ",
            appsdb.ApplicationsDatabase().get_pretty_app_names(), True)

        blacklist = ""
        if confirm("Would you like to specify any applications you would "
                        "NOT like to sync?"):
            blacklist = choose("Choose any of the follwing "
            "deliminated by a space): ",
            appsdb.ApplicationsDatabase().get_pretty_app_names(), True)

        custom_apps = {} # {app_name: [config files]}
        if confirm("Now, would you like to add any applications not "
                         "currently supported by Mackup?"):
            print "Enter nothing to indicate your done"
            while True:
                name = raw_input("Application name: ")
                if not name:
                    break
                config_files = raw_input("Please enter the names of all the "
                "configuration files, delemenated by a space").split()
                custom_apps.update({name: config_files})
        with open(os.path.join(os.path.expanduser("~"),
                   MACKUP_CONFIG_FILE), "w") as config_file:
            config_file.write("[storage]\n")
            config_file.write("engine = {}\npath = {}\n".format(
                                                      storage_type, path))
            config_file.write("directory = {}\n".format(directory))
            if whitelist:
                config_file.write("[applications_to_sync]\n")
                config_file.write("\n".join(whitelist))
            if blacklist:
                config_file.write("[applications_to_ignore]\n")
                config_file.write("\n".join(blacklist))
        if custom_apps:
            os.makedirs(os.path.join(os.path.expanduser("~"), CUSTOM_APPS_DIR))
            for name, config_files in custom_apps.iteritems():
                with open(os.path.join(os.path.expanduser("~"),
                CUSTOM_APPS_DIR, "-".join(app.name.split())), "w") as (
                custom_app_file):
                    custom_app_file.write("[application]\n")
                    custom_app_file.write("name = {}\n".format(name))
                    custom_app_file.write("[configuration_files]")
                    custom_app_file.write("\n".join(config_files))

class ConfigError(Exception):

    """Exception used for handle errors in the configuration."""

    pass
