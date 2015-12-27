"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2015 Laurent Raufaste <http://glop.org/>

Usage:
  mackup list
  mackup [options] backup [--all | <app>...]
  mackup [options] restore [--all | <app>...]
  mackup [options] uninstall [--all | <app>...]
  mackup (-h | --help)
  mackup --version

Options:
  -h --help     Show this screen.
  -f --force    Force every question asked to be answered with "Yes".
  -n --dry-run  Show steps without executing.
  -v --verbose  Show additional details.
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


class ColorFormatCodes:
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    NORMAL = '\033[0m'


def header(str):
    return ColorFormatCodes.BLUE + str + ColorFormatCodes.NORMAL


def bold(str):
    return ColorFormatCodes.BOLD + str + ColorFormatCodes.NORMAL


def main():
    """Main function."""
    # Get the command line arg
    args = docopt(__doc__, version="Mackup {}".format(VERSION))

    mckp = Mackup()
    app_db = ApplicationsDatabase()

    def printAppHeader(app_name):
        if verbose:
            print(("\n{0} {1} {0}").format(header("---"), bold(app_name)))

    # If we want to answer mackup with "yes" for each question
    if args['--force']:
        utils.FORCE_YES = True

    dry_run = args['--dry-run']

    verbose = args['--verbose']

    if args['backup']:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Get app names from the command line,
        # otherwise from the configurations
        if args['<app>']:
            app_names = args['<app>'];
        elif args['--all']:
            app_names = mckp.get_apps_to_backup();

        # Backup each application
        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp,
                                     app_db.get_files(app_name),
                                     dry_run,
                                     verbose)
            printAppHeader(app_name)
            app.backup()

    elif args['restore']:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        # Get app names from the command line,
        # otherwise from the configurations
        if args['<app>']:
            app_names = args['<app>'];
        elif args['--all']:
            # Restore the Mackup config before any other config, as we might need
            # it to know about custom settings
            mackup_app = ApplicationProfile(mckp,
                                            app_db.get_files(MACKUP_APP_NAME),
                                            dry_run,
                                            verbose)
            printAppHeader(MACKUP_APP_NAME)
            mackup_app.restore()

            # Initialize the apps db again, the Mackup config might have changed
            mckp = Mackup()
            app_db = ApplicationsDatabase()

            # Restore the rest of the app configs, using the restored Mackup config
            app_names = mckp.get_apps_to_backup()
            # Mackup has already been done
            app_names.discard(MACKUP_APP_NAME)

        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp,
                                     app_db.get_files(app_name),
                                     dry_run,
                                     verbose)
            printAppHeader(app_name)
            app.restore()

    elif args['uninstall']:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if dry_run or (
           utils.confirm("Attempting to uninstall Mackup.\n"
                         "Configuration files, settings and dotfiles"
                         " managed by Mackup will be unlinked and moved back"
                         " to their original locations.\n"
                         "Are you sure ?")):

            # Get app names from the command line,
            # otherwise from the configurations
            if args['<app>']:
                app_names = args['<app>'];
            elif args['--all']:
                # Uninstall the apps except Mackup, which we'll uninstall last, to
                # keep the settings as long as possible
                app_names = mckp.get_apps_to_backup()
                app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(app_names):
                app = ApplicationProfile(mckp,
                                         app_db.get_files(app_name),
                                         dry_run,
                                         verbose)
                printAppHeader(app_name)
                app.uninstall()

            # Uninstall the Mackup config last
            mackup_app = ApplicationProfile(mckp,
                                            app_db.get_files(MACKUP_APP_NAME),
                                            dry_run,
                                            verbose)
            mackup_app.uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            print("All files have been unlinked into their original locations.\n"
                  "Mackup can now be safely uninstall.")

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
