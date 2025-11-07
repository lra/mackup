"""
The applications database.

The Applications Database provides an easy to use interface to load application
data from the Mackup Database (files).
"""

import os
from typing import Dict, Set, Union

import configparser

from .constants import APPS_DIR
from .constants import CUSTOM_APPS_DIR


class ApplicationsDatabase:
    """Database containing all the configured applications."""

    def __init__(self) -> None:
        """Create a ApplicationsDatabase instance."""
        # Build the dict that will contain the properties of each application
        self.apps: Dict[str, Dict[str, Union[str, Set[str]]]] = {}

        for config_file in ApplicationsDatabase.get_config_files():
            config: configparser.ConfigParser = configparser.ConfigParser(allow_no_value=True)

            # Needed to not lowercase the configuration_files in the ini files
            config.optionxform = str  # type: ignore

            if config.read(config_file):
                # Get the filename without the directory name
                filename: str = os.path.basename(config_file)
                # The app name is the cfg filename with the extension
                app_name: str = filename[: -len(".cfg")]

                # Start building a dict for this app
                self.apps[app_name] = {}

                # Add the fancy name for the app, for display purpose
                app_pretty_name: str = config.get("application", "name")
                self.apps[app_name]["name"] = app_pretty_name

                # Add the configuration files to sync
                self.apps[app_name]["configuration_files"] = set()
                if config.has_section("configuration_files"):
                    for path in config.options("configuration_files"):
                        if path.startswith("/"):
                            raise ValueError(
                                "Unsupported absolute path: {}".format(path)
                            )
                        self.apps[app_name]["configuration_files"].add(path)

                # Add the XDG configuration files to sync
                home: str = os.path.expanduser("~/")
                failobj: str = "{}.config".format(home)
                xdg_config_home: str = os.environ.get("XDG_CONFIG_HOME", failobj)
                if not xdg_config_home.startswith(home):
                    raise ValueError(
                        "$XDG_CONFIG_HOME: {} must be "
                        "somewhere within your home "
                        "directory: {}".format(xdg_config_home, home)
                    )
                if config.has_section("xdg_configuration_files"):
                    for path in config.options("xdg_configuration_files"):
                        if path.startswith("/"):
                            raise ValueError(
                                "Unsupported absolute path: " "{}".format(path)
                            )
                        path = os.path.join(xdg_config_home, path)
                        path = path.replace(home, "")
                        (self.apps[app_name]["configuration_files"].add(path))

    @staticmethod
    def get_config_files() -> Set[str]:
        """
        Return the application configuration files.

        Return a list of configuration files describing the apps supported by
        Mackup. The files returned are absolute full path to those files.
        e.g. /usr/lib/mackup/applications/bash.cfg

        Only one config file per application should be returned, custom config
        having a priority over stock config.

        Returns:
            set of strings.
        """
        # Configure the config parser
        apps_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), APPS_DIR)
        custom_apps_dir: str = os.path.join(os.environ["HOME"], CUSTOM_APPS_DIR)

        # List of stock application config files
        config_files: Set[str] = set()

        # Temp list of user added app config file names
        custom_files: Set[str] = set()

        # Get the list of custom application config files first
        if os.path.isdir(custom_apps_dir):
            for filename in os.listdir(custom_apps_dir):
                if filename.endswith(".cfg"):
                    config_files.add(os.path.join(custom_apps_dir, filename))
                    # Also add it to the set of custom apps, so that we don't
                    # add the stock config for the same app too
                    custom_files.add(filename)

        # Add the default provided app config files, but only if those are not
        # customized, as we don't want to overwrite custom app config.
        for filename in os.listdir(apps_dir):
            if filename.endswith(".cfg") and filename not in custom_files:
                config_files.add(os.path.join(apps_dir, filename))

        return config_files

    def get_name(self, name: str) -> str:
        """
        Return the fancy name of an application.

        Args:
            name (str)

        Returns:
            str
        """
        value = self.apps[name]["name"]
        assert isinstance(value, str)
        return value

    def get_files(self, name: str) -> Set[str]:
        """
        Return the list of config files of an application.

        Args:
            name (str)

        Returns:
            set of str.
        """
        value = self.apps[name]["configuration_files"]
        assert isinstance(value, set)
        return value

    def get_app_names(self) -> Set[str]:
        """
        Return application names.

        Return the list of application names that are available in the
        database.

        Returns:
            set of str.
        """
        app_names: Set[str] = set()
        for name in self.apps:
            app_names.add(name)

        return app_names

    def get_pretty_app_names(self) -> Set[str]:
        """
        Return the list of pretty app names that are available in the database.

        Returns:
            set of str.
        """
        pretty_app_names: Set[str] = set()
        for app_name in self.get_app_names():
            pretty_app_names.add(self.get_name(app_name))

        return pretty_app_names
