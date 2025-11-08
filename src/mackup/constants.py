"""Constants used in Mackup."""

from importlib.metadata import version

# Support platforms
PLATFORM_DARWIN: str = "Darwin"
PLATFORM_LINUX: str = "Linux"

# Directory containing the application configs
APPS_DIR: str = "applications"

# Mackup application name
MACKUP_APP_NAME: str = "mackup"

# Default Mackup backup path where it stores its files in Dropbox
MACKUP_BACKUP_PATH: str = "Mackup"

# Mackup config file
MACKUP_CONFIG_FILE: str = ".mackup.cfg"

# Current version
VERSION: str = version(MACKUP_APP_NAME)

# Directory that can contains user defined app configs
CUSTOM_APPS_DIR: str = ".mackup"

# Supported engines
ENGINE_DROPBOX: str = "dropbox"
ENGINE_FS: str = "file_system"
ENGINE_GDRIVE: str = "google_drive"
ENGINE_ICLOUD: str = "icloud"

DOCUMENTATION_URL: str = "https://github.com/lra/mackup/blob/master/doc/README.md"

# Error message displayed when mackup can't find the storage specified
# in the config (or the default one).
ERROR_UNABLE_TO_FIND_STORAGE: str = (
    "Unable to find your {provider} =(\n"
    "If this is the first time you use %s, you may want "
    "to use another provider.\n"
    "Take a look at the documentation [1] to know more about "
    "how to configure mackup.\n\n"
    "[1]: %s" % (MACKUP_APP_NAME, DOCUMENTATION_URL)
)
