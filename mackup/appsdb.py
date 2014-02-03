"""
The Applications Database provides an easy to use interface to load application
data from the Mackup Database (files)
"""
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


from .constants import APPS_DIR
from .constants import CUSTOM_APPS_DIR


class ApplicationsDatabase(object):
    """Database containing all the configured applications"""

    def __init__(self):
        """
        Create a ApplicationsDatabase instance
        """
        # Configure the config parser
        apps_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                APPS_DIR)
        custom_apps_dir = os.path.join(os.environ['HOME'], CUSTOM_APPS_DIR)

        # Build the list of stock application config files
        config_files = []
        for filename in os.listdir(apps_dir):
            if filename.endswith('.cfg'):
                config_files.append(os.path.join(apps_dir, filename))

        # Append the list of custom application config files
        if os.path.isdir(custom_apps_dir):
            for filename in os.listdir(custom_apps_dir):
                if filename.endswith('.cfg'):
                    config_files.append(os.path.join(custom_apps_dir,
                                                     filename))

        # Build the dict that will contain the properties of each application
        self.apps = dict()

        for config_file in config_files:
            config = configparser.SafeConfigParser(allow_no_value=True)

            # Needed to not lowercase the configuration_files in the ini files
            config.optionxform = str

            if config.read(config_file):
                # Get the filename without the directory name
                filename = os.path.basename(config_file)
                # The app name is the cfg filename with the extension
                app_name = filename[:-len('.cfg')]

                # Start building a dict for this app
                self.apps[app_name] = dict()

                # Add the fancy name for the app, for display purpose
                app_pretty_name = config.get('application', 'name')
                self.apps[app_name]['name'] = app_pretty_name

                # Add the configuration files to sync
                self.apps[app_name]['configuration_files'] = set()
                if config.has_section('configuration_files'):
                    for paths in config.options('configuration_files'):
                        self.apps[app_name]['configuration_files'].add(paths)

    def get_name(self, name):
        """
        Return the fancy name of an application

        Args:
            name (str)

        Returns:
            str
        """
        return self.apps[name]['name']

    def get_files(self, name):
        """
        Return the list of config files of an application

        Args:
            name (str)

        Returns:
            list(str)
        """
        return list(self.apps[name]['configuration_files'])

    def get_app_names(self):
        """
        Return the list of application names that are available in the database

        Returns:
            list(str)
        """
        app_names = []
        for name in self.apps:
            app_names.append(name)

        return app_names

    def get_pretty_app_names(self):
        """
        Return the list of pretty app names that are available in the database

        Returns:
            list(str)
        """
        pretty_app_names = []
        for app_name in self.get_app_names():
            pretty_app_names.append(self.get_name(app_name))

        return pretty_app_names
