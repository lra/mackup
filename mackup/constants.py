"""Constants used in Mackup."""
# Current version
VERSION = "0.8.37"

# Support platforms
PLATFORM_DARWIN = "Darwin"
PLATFORM_LINUX = "Linux"

# Directory containing the application configs
APPS_DIR = "applications"

# Mackup application name
MACKUP_APP_NAME = "mackup"

# Default Mackup backup path where it stores its files in Dropbox
MACKUP_BACKUP_PATH = "Mackup"

# Mackup config file
MACKUP_CONFIG_FILE = ".mackup.cfg"

# Directory that can contains user defined app configs
CUSTOM_APPS_DIR = ".mackup"

# Supported engines
ENGINE_COPY = "copy"
ENGINE_DROPBOX = "dropbox"
ENGINE_FS = "file_system"
ENGINE_GDRIVE = "google_drive"
ENGINE_ICLOUD = "icloud"

DOCUMENTATION_URL = "https://github.com/lra/mackup/blob/master/doc/README.md"

# Error message displayed when mackup can't find the storage specified
# in the config (or the default one).
ERROR_UNABLE_TO_FIND_STORAGE = (
    "Unable to find your {provider} =(\n"
    "If this is the first time you use %s, you may want "
    "to use another provider.\n"
    "Take a look at the documentation [1] to know more about "
    "how to configure mackup.\n\n"
    "[1]: %s" % (MACKUP_APP_NAME, DOCUMENTATION_URL)
)
