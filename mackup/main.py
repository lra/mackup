"""
Keep your application settings in sync.

Copyright (C) 2013 Laurent Raufaste <http://glop.org/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

from .appsdb import ApplicationsDatabase
from .application import ApplicationProfile
from .constants import (BACKUP_MODE,
                        RESTORE_MODE,
                        UNINSTALL_MODE,
                        LIST_MODE,
                        STATUS_MODE,
                        VERSION)
from .mackup import Mackup
from . import utils
from . import config


def list_mode():
    """
    List the supported applications
    """
    app_db = ApplicationsDatabase()

    # Display the list of supported applications
    output = "Supported applications:\n"
    for app_name in sorted(app_db.get_app_names()):
        output += " - {}\n".format(app_name)
    output += "\n"
    output += ("{} applications supported in Mackup v{}"
               .format(len(app_db.get_app_names()), VERSION))
    print output


def status_mode():
    """
    Display the storage engine and the application status
    """
    cfg = config.Config()
    mckp = Mackup()
    app_db = ApplicationsDatabase()
    dropbox_path = utils.get_dropbox_folder_location()
    gdrive_path = utils.get_google_drive_folder_location()

    print "Storage engines supported:"
    if dropbox_path:
        print " - dropbox: Available under {}".format(dropbox_path)
    else:
        print " - dropbox: Not available"
    if gdrive_path:
        print " - google_drive: Available under {}".format(gdrive_path)
    else:
        print " - google_drive: Not available"
    print " - file_system: Available below {}".format(os.environ['HOME'])
    print
    print "Engine selected: {}".format(cfg.engine)
    print "Files location: {}".format(cfg.fullpath)
    print

    # Check the env where the command is being run
    mckp.check_for_usable_restore_env()

    print "Applications status:"
    for app_name in mckp.get_apps_to_backup():
        print " - {}".format(app_name)


def backup_mode():
    """
    Backup application configs from the home into the storage
    """
    mckp = Mackup()
    app_db = ApplicationsDatabase()

    # Check the env where the command is being run
    mckp.check_for_usable_backup_env()

    # Backup each application
    for app_name in mckp.get_apps_to_backup():
        app = ApplicationProfile(mckp, app_db.get_files(app_name))
        app.backup()


def restore_mode():
    """
    Restore application configs from the storage back into home
    """
    mckp = Mackup()
    app_db = ApplicationsDatabase()

    # Check the env where the command is being run
    mckp.check_for_usable_restore_env()

    for app_name in app_db.get_app_names():
        app = ApplicationProfile(mckp, app_db.get_files(app_name))
        app.restore()


def uninstall_mode():
    """
    Copy back all the app configs from the storage into home
    """
    mckp = Mackup()
    app_db = ApplicationsDatabase()

    # Check the env where the command is being run
    mckp.check_for_usable_restore_env()

    if utils.confirm("You are going to uninstall Mackup.\n"
                     "Every configuration file, setting and dotfile"
                     " managed by Mackup will be unlinked and moved back"
                     " to their original place, in your home folder.\n"
                     "Are you sure ?"):
        for app_name in app_db.get_app_names():
            app = ApplicationProfile(mckp, app_db.get_files(app_name))
            app.uninstall()

        # Delete the Mackup folder in Dropbox
        # Don't delete this as there might be other Macs that aren't
        # uninstalled yet
        # delete(mckp.mackup_folder)

        print ("\n"
               "All your files have been put back into place. You can now"
               " safely uninstall Mackup.\n"
               "\n"
               "Thanks for using Mackup !"
               .format(os.path.abspath(__file__)))


def main():
    """Main function"""

    # Get the command line arg
    args = utils.parse_cmdline_args()

    if args.mode == LIST_MODE:
        list_mode()
    elif args.mode == STATUS_MODE:
        status_mode()
    elif args.mode == BACKUP_MODE:
        backup_mode()
    elif args.mode == RESTORE_MODE:
        restore_mode()
    elif args.mode == UNINSTALL_MODE:
        uninstall_mode()
    else:
        raise ValueError("Unsupported mode: {}".format(args.mode))
