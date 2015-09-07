"""Constants used in Mackup."""
# Current version
VERSION = '0.8.11'

# Support platforms
PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

# Directory containing the application configs
APPS_DIR = 'applications'

# Mackup application name
MACKUP_APP_NAME = 'mackup'

# Default Mackup backup path where it stores its files in Dropbox
MACKUP_BACKUP_PATH = 'Mackup'

# Mackup config file for non XDG users
MACKUP_CONFIG_FILE = '.mackup.cfg'
# Directory that can contains user defined app configs; for non XDG users
CUSTOM_APPS_DIR = '.mackup'

# Mackup config file; for XDG users
XDG_MACKUP_CONFIG_FILE = 'mackup.cfg'
# Directory that can contains user defined app configs; for XDG users
XDG_CUSTOM_APPS_DIR = 'mackup'

# Supported engines
ENGINE_DROPBOX = 'dropbox'
ENGINE_GDRIVE = 'google_drive'
ENGINE_BOX = 'box'
ENGINE_COPY = 'copy'
ENGINE_ICLOUD = 'icloud'
ENGINE_FS = 'file_system'
