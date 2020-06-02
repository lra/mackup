"""Package used to manage the .mackup.cfg config file."""

import os
import os.path

from .constants import (
    CUSTOM_APPS_DIR,
    MACKUP_BACKUP_PATH,
    MACKUP_CONFIG_FILE,
    ENGINE_DROPBOX,
    ENGINE_GDRIVE,
    ENGINE_COPY,
    ENGINE_ICLOUD,
    ENGINE_FS,
)

from .utils import (
    error,
    get_dropbox_folder_location,
    get_copy_folder_location,
    get_google_drive_folder_location,
    get_icloud_folder_location,
)

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


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

        # Get colors for cli
        self._cli_colors = self._parse_cli_colors()

    @property
    def engine(self):
        """
        The engine used by the storage.

        ENGINE_DROPBOX, ENGINE_GDRIVE, ENGINE_COPY, ENGINE_ICLOUD or ENGINE_FS.

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
        parser.read(os.path.join(os.path.join(os.environ["HOME"], filename)))

        return parser

    def _warn_on_old_config(self):
        """Warn the user if an old config format is detected."""
        # Is an old setion is in the config file ?
        old_sections = ["Allowed Applications", "Ignored Applications"]
        for old_section in old_sections:
            if self._parser.has_section(old_section):
                error(
                    "Old config file detected. Aborting.\n"
                    "\n"
                    "An old section (e.g. [Allowed Applications]"
                    " or [Ignored Applications] has been detected"
                    " in your {} file.\n"
                    "I'd rather do nothing than do something you"
                    " do not want me to do.\n"
                    "\n"
                    "Please read the up to date documentation on"
                    " <https://github.com/lra/mackup> and migrate"
                    " your configuration file.".format(MACKUP_CONFIG_FILE)
                )

    def _parse_engine(self):
        """
        Parse the storage engine in the config.

        Returns:
            str
        """
        if self._parser.has_option("storage", "engine"):
            engine = str(self._parser.get("storage", "engine"))
        else:
            engine = ENGINE_DROPBOX

        assert isinstance(engine, str)

        if engine not in [
            ENGINE_DROPBOX,
            ENGINE_GDRIVE,
            ENGINE_COPY,
            ENGINE_ICLOUD,
            ENGINE_FS,
        ]:
            raise ConfigError("Unknown storage engine: {}".format(engine))

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
        elif self.engine == ENGINE_FS:
            if self._parser.has_option("storage", "path"):
                cfg_path = self._parser.get("storage", "path")
                path = os.path.join(os.environ["HOME"], cfg_path)
            else:
                raise ConfigError(
                    "The required 'path' can't be found while"
                    " the 'file_system' engine is used."
                )

        return str(path)

    def _parse_directory(self):
        """
        Parse the storage directory in the config.

        Returns:
            str
        """
        if self._parser.has_option("storage", "directory"):
            directory = self._parser.get("storage", "directory")
            # Don't allow CUSTOM_APPS_DIR as a storage directory
            if directory == CUSTOM_APPS_DIR:
                raise ConfigError(
                    "{} cannot be used as a storage directory.".format(CUSTOM_APPS_DIR)
                )
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
        section_title = "applications_to_ignore"
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
        section_title = "applications_to_sync"
        if self._parser.has_section(section_title):
            apps_to_sync = set(self._parser.options(section_title))

        return apps_to_sync

    def _parse_cli_colors(self):
        colors = {
            "text": "[1;33m",
            "filename": "[1;34m",
            "filename_path_separator": "[1;35m",
            "name": "[1;34m",
            "item_bullet": "[1;32m",
            "item_header": "[1;36m",
            "header_app_name": "[1;34m",
            "reset": "[0m",
        }

        if self._parser.has_section("colors"):
            if self._parser.has_option("colors", "text"):
                colors["text"] = "[" + str(self._parser.get("colors", "text")) + "m"

            if self._parser.has_option("colors", "filename"):
                colors["filename"] = (
                    "[" + str(self._parser.get("colors", "filename")) + "m"
                )

            if self._parser.has_option("colors", "filename_path_separator"):
                colors["filename_path_separator"] = (
                    "["
                    + str(self._parser.get("colors", "filename_path_separator"))
                    + "m"
                )

            if self._parser.has_option("colors", "name"):
                colors["name"] = "[" + str(self._parser.get("colors", "name")) + "m"

            if self._parser.has_option("colors", "item_bullet"):
                colors["item_bullet"] = (
                    "[" + str(self._parser.get("colors", "item_bullet")) + "m"
                )

            if self._parser.has_option("colors", "item_header"):
                colors["item_header"] = (
                    "[" + str(self._parser.get("colors", "item_header")) + "m"
                )

            if self._parser.has_option("colors", "header_app_name"):
                colors["header_app_name"] = (
                    "[" + str(self._parser.get("colors", "header_app_name")) + "m"
                )

        if "MACKUP_COLORS" in os.environ:
            lsc = os.environ["MACKUP_COLORS"]
            for setting in lsc.split(":"):
                if not setting:
                    continue  # skip empty

                key, code = setting.split("=")

                if not key or not code:
                    continue  # skip empty

                if key in [
                    "text",
                    "filename",
                    "filename_path_separator",
                    "name",
                    "item_bullet",
                    "item_header",
                    "header_app_name",
                ]:
                    colors[key] = "[" + code + "m"

        return colors


class ConfigError(Exception):

    """Exception used for handle errors in the configuration."""

    pass
