"""
The applications database.

The Applications Database provides an easy to use interface to load application
data from the Mackup Database (files).
"""

import configparser
import os
from typing import Union

from .constants import APPS_DIR, CUSTOM_APPS_DIR, CUSTOM_APPS_DIR_XDG


class ApplicationsDatabase:
    """Database containing all the configured applications."""

    def __init__(self) -> None:
        """Create a ApplicationsDatabase instance."""
        # Build the dict that will contain the properties of each application
        self.apps: dict[str, dict[str, Union[str, set[str]]]] = {}

        for config_file in ApplicationsDatabase.get_config_files():
            config: configparser.ConfigParser = configparser.ConfigParser(
                allow_no_value=True
            )

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
                config_files: set[str] = set()
                self.apps[app_name]["configuration_files"] = config_files
                if config.has_section("configuration_files"):
                    for path in config.options("configuration_files"):
                        if path.startswith("/"):
                            raise ValueError(
                                f"Unsupported absolute path: {path}",
                            )
                        config_files.add(path)

                # Add the XDG configuration files to sync
                home: str = os.path.expanduser("~/")
                failobj: str = f"{home}.config"
                xdg_config_home: str = os.environ.get("XDG_CONFIG_HOME", failobj)
                if not xdg_config_home.startswith(home):
                    raise ValueError(
                        f"$XDG_CONFIG_HOME: {xdg_config_home} must be somewhere "
                        f"within your home directory: {home}",
                    )
                if config.has_section("xdg_configuration_files"):
                    for path in config.options("xdg_configuration_files"):
                        if path.startswith("/"):
                            raise ValueError(
                                f"Unsupported absolute path: {path}",
                            )
                        path = os.path.join(xdg_config_home, path)
                        path = path.replace(home, "")
                        config_files.add(path)

    @staticmethod
    def get_config_files() -> set[str]:
        """
        Return the application configuration files.

        Return a list of configuration files describing the apps supported by
        Mackup. The files returned are absolute full path to those files.
        e.g. /usr/lib/mackup/applications/bash.cfg

        Only one config file per application should be returned, custom config
        having a priority over stock config. Legacy custom apps directory
        (~/.mackup/) takes priority over XDG location.

        Returns:
            set of strings.
        """
        # Configure the config parser
        apps_dir: str = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), APPS_DIR
        )

        # Legacy custom apps directory: ~/.mackup/
        legacy_custom_apps_dir: str = os.path.join(os.environ["HOME"], CUSTOM_APPS_DIR)

        # XDG custom apps directory: $XDG_CONFIG_HOME/mackup/applications/
        xdg_config_home: str = os.environ.get(
            "XDG_CONFIG_HOME", os.path.join(os.environ["HOME"], ".config")
        )
        xdg_custom_apps_dir: str = os.path.join(xdg_config_home, CUSTOM_APPS_DIR_XDG)

        # List of stock application config files
        config_files: set[str] = set()

        # Temp list of user added app config file names
        custom_files: set[str] = set()

        # Get the list of custom application config files from legacy directory first
        # (legacy takes priority over XDG)
        if os.path.isdir(legacy_custom_apps_dir):
            for filename in os.listdir(legacy_custom_apps_dir):
                if filename.endswith(".cfg"):
                    config_files.add(os.path.join(legacy_custom_apps_dir, filename))
                    custom_files.add(filename)

        # Get custom application config files from XDG directory
        # (only if not already in legacy directory)
        if os.path.isdir(xdg_custom_apps_dir):
            for filename in os.listdir(xdg_custom_apps_dir):
                if filename.endswith(".cfg") and filename not in custom_files:
                    config_files.add(os.path.join(xdg_custom_apps_dir, filename))
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

    def get_files(self, name: str) -> set[str]:
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

    def get_app_names(self) -> set[str]:
        """
        Return application names.

        Return the list of application names that are available in the
        database.

        Returns:
            set of str.
        """
        app_names: set[str] = set()
        for name in self.apps:
            app_names.add(name)

        return app_names

    def get_pretty_app_names(self) -> set[str]:
        """
        Return the list of pretty app names that are available in the database.

        Returns:
            set of str.
        """
        pretty_app_names: set[str] = set()
        for app_name in self.get_app_names():
            pretty_app_names.add(self.get_name(app_name))

        return pretty_app_names
