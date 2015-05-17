"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2015 Laurent Raufaste <http://glop.org/>

Usage:
  mackup list
  mackup backup
  mackup restore
  mackup uninstall
  mackup (-h | --help)
  mackup --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Modes of action:
 1. list: display a list of all supported applications.
 2. backup: sync your conf files to your synced storage, use this the 1st time
    you use Mackup. (Note that by default this will sync private keys used by
    OpenSSH and GnuPG.)
 3. restore: link the conf files already in your synced storage on your system,
    use it on any new system you use.
 4. uninstall: reset everything as it was before using Mackup.

By default, Mackup syncs all application data (including private keys!) via
Dropbox, but may be configured to exclude applications or use a different
backend with a .mackup.cfg file.

See https://github.com/lra/mackup/tree/master/doc for more information.

"""
from docopt import docopt
from .appsdb import ApplicationsDatabase
from .application import ApplicationProfile
from .constants import MACKUP_APP_NAME, VERSION
from .mackup import Mackup
from . import utils


def main():
    """Main function."""
    # Get the command line arg
    args = docopt(__doc__, version="Mackup {}".format(VERSION))

    mckp = Mackup()
    app_db = ApplicationsDatabase()

    if args['backup']:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Backup each application
        for app_name in mckp.get_apps_to_backup():
            app = ApplicationProfile(mckp, app_db.get_files(app_name))
            app.backup()

    elif args['restore']:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        # Restore the Mackup config before any other config, as we might need
        # it to know about custom settings
        mackup_app = ApplicationProfile(mckp,
                                        app_db.get_files(MACKUP_APP_NAME))
        mackup_app.restore()

        # Initialize again the apps db, as the Mackup config might have changed
        # it
        mckp = Mackup()
        app_db = ApplicationsDatabase()

        # Restore the rest of the app configs, using the restored Mackup config
        app_names = mckp.get_apps_to_backup()
        # Mackup has already been done
        app_names.discard(MACKUP_APP_NAME)

        for app_name in app_names:
            app = ApplicationProfile(mckp, app_db.get_files(app_name))
            app.restore()

    elif args['uninstall']:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if utils.confirm("You are going to uninstall Mackup.\n"
                         "Every configuration file, setting and dotfile"
                         " managed by Mackup will be unlinked and moved back"
                         " to their original place, in your home folder.\n"
                         "Are you sure ?"):

            # Uninstall the apps except Mackup, which we'll uninstall last, to
            # keep the settings as long as possible
            app_names = mckp.get_apps_to_backup()
            app_names.discard(MACKUP_APP_NAME)
            for app_name in mckp.get_apps_to_backup():
                app = ApplicationProfile(mckp, app_db.get_files(app_name))
                app.uninstall()

            # Restore the Mackup config before any other config, as we might
            # need it to know about custom settings
            mackup_app = ApplicationProfile(mckp,
                                            app_db.get_files(MACKUP_APP_NAME))
            mackup_app.uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            print("\n"
                  "All your files have been put back into place. You can now"
                  " safely uninstall Mackup.\n"
                  "\n"
                  "Thanks for using Mackup !")

    elif args['list']:
        # Display the list of supported applications
        mckp.check_for_usable_environment()
        output = "Supported applications:\n"
        for app_name in sorted(app_db.get_app_names()):
            output += " - {}\n".format(app_name)
        output += "\n"
        output += ("{} applications supported in Mackup v{}"
                   .format(len(app_db.get_app_names()), VERSION))
        print(output)

    # Delete the tmp folder
    mckp.clean_temp_folder()
