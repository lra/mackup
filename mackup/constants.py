"""Constants used in Mackup."""
# Current version
VERSION = '0.8.3'

# Mode used to list supported applications
LIST_MODE = 'list'

# Mode used to backup files to Dropbox
BACKUP_MODE = 'backup'

# Mode used to restore files from Dropbox
RESTORE_MODE = 'restore'

# Mode used to remove Mackup and reset and config file
UNINSTALL_MODE = 'uninstall'

# Support platforms
PLATFORM_DARWIN = 'Darwin'
PLATFORM_LINUX = 'Linux'

# Directory containing the application configs
APPS_DIR = 'applications'

# Mackup application name
MACKUP_APP_NAME = 'mackup'

# Default Mackup backup path where it stores its files in Dropbox
MACKUP_BACKUP_PATH = 'Mackup'

# Mackup config file
MACKUP_CONFIG_FILE = '.mackup.cfg'

# Directory that can contains user defined app configs
CUSTOM_APPS_DIR = '.mackup'

# Supported engines
ENGINE_DROPBOX = 'dropbox'
ENGINE_GDRIVE = 'google_drive'
ENGINE_COPY = 'copy'
ENGINE_FS = 'file_system'
