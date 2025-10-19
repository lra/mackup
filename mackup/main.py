"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2025 Laurent Raufaste <http://glop.org/>

Usage:
  mackup list
  mackup show <application>
  mackup [options] backup
  mackup [options] restore
  mackup [options] link install
  mackup [options] link
  mackup [options] link uninstall
  mackup (-h | --help)

Options:
  -h --help     Show this screen.
  -f --force    Force every question asked to be answered with "Yes".
  --force-no    Force every question asked to be answered with "No".
  -r --root     Allow mackup to be run as superuser.
  -n --dry-run  Show steps without executing.
  -v --verbose  Show additional details.
  --version     Show version.

Modes of action:
 - mackup list: display a list of all supported applications.
 - mackup show: display the details for a supported application.
 - mackup backup: copy local config files in the configured remote folder.
 - mackup restore: copy config files from the configured remote folder locally.
 - mackup link install: moves local config files in remote folder, and links them.
 - mackup link: links local config files from the remote folder.
 - mackup link uninstall: removes the links and copy config files from the remote folder locally.

By default, Mackup syncs all application data via
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
import sys
from typing import Dict, Any


class ColorFormatCodes:
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    NORMAL = "\033[0m"


def header(text: str) -> str:
    return ColorFormatCodes.BLUE + text + ColorFormatCodes.NORMAL


def bold(text: str) -> str:
    return ColorFormatCodes.BOLD + text + ColorFormatCodes.NORMAL


def main() -> None:
    """Main function."""
    # Get the command line arg
    args: Dict[str, Any] = docopt(__doc__, version="Mackup {}".format(VERSION))

    mckp = Mackup()
    app_db = ApplicationsDatabase()

    def printAppHeader(app_name: str) -> None:
        if verbose:
            print(("\n{0} {1} {0}").format(header("---"), bold(app_name)))

    # If we want to answer mackup with "yes" for each question
    if args["--force"]:
        utils.FORCE_YES = True

     # If we want to answer mackup with "no" for each question
    if args['--force-no']:
        utils.FORCE_NO = True

    # Allow mackup to be run as root
    if args["--root"]:
        utils.CAN_RUN_AS_ROOT = True

    dry_run = args["--dry-run"]

    verbose = args["--verbose"]

    # mackup list
    if args["list"]:
        # Display the list of supported applications
        mckp.check_for_usable_environment()
        output = "Supported applications:\n"
        for app_name in sorted(app_db.get_app_names()):
            output += " - {}\n".format(app_name)
        output += "\n"
        output += "{} applications supported in Mackup v{}".format(
            len(app_db.get_app_names()), VERSION
        )
        print(output)

    # mackup show <application>
    elif args["show"]:
        mckp.check_for_usable_environment()
        app_name = args["<application>"]

        # Make sure the app exists
        if app_name not in app_db.get_app_names():
            sys.exit("Unsupported application: {}".format(app_name))
        print("Name: {}".format(app_db.get_name(app_name)))
        print("Configuration files:")
        for file in app_db.get_files(app_name):
            print(" - {}".format(file))

    # mackup backup
    elif args["backup"]:
        mckp.check_for_usable_backup_env()

        # Create a backup of the files of each application
        for app_name in sorted(mckp.get_apps_to_backup()):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            printAppHeader(app_name)
            app.copy_files_to_mackup_folder()

    # mackup restore
    elif args["restore"]:
        mckp.check_for_usable_backup_env()

        # Recover a backup of the files of each application
        for app_name in sorted(mckp.get_apps_to_backup()):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            printAppHeader(app_name)
            app.copy_files_from_mackup_folder()

    # mackup link install
    elif args["link"] and args["install"]:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Create a link for each application
        for app_name in sorted(mckp.get_apps_to_backup()):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            printAppHeader(app_name)
            app.link_install()

    # mackup link uninstall
    elif args["link"] and args["uninstall"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if dry_run or (
            utils.confirm(
                "You are going to uninstall Mackup.\n"
                "Every configuration file, setting and dotfile"
                " managed by Mackup will be unlinked and copied back"
                " to their original place, in your home folder.\n"
                "Are you sure?"
            )
        ):
            # Uninstall the apps except Mackup, which we'll uninstall last, to
            # keep the settings as long as possible
            app_names = mckp.get_apps_to_backup()
            app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(app_names):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose
                )
                printAppHeader(app_name)
                app.link_uninstall()

            # Restore the Mackup config before any other config, as we might
            # need it to know about custom settings
            mackup_app = ApplicationProfile(
                mckp, app_db.get_files(MACKUP_APP_NAME), dry_run, verbose
            )
            mackup_app.link_uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            print(
                "\n"
                "All your files have been put back into place. You can now"
                " safely uninstall Mackup.\n"
                "\n"
                "Thanks for using Mackup!"
            )

    # mackup link
    elif args["link"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        # Restore the Mackup config before any other config, as we might need
        # it to know about custom settings
        mackup_app = ApplicationProfile(
            mckp, app_db.get_files(MACKUP_APP_NAME), dry_run, verbose
        )
        printAppHeader(MACKUP_APP_NAME)
        mackup_app.link()

        # Initialize again the apps db, as the Mackup config might have changed
        # it
        mckp = Mackup()
        app_db = ApplicationsDatabase()

        # Restore the rest of the app configs, using the restored Mackup config
        app_names = mckp.get_apps_to_backup()
        # Mackup has already been done
        app_names.discard(MACKUP_APP_NAME)

        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            printAppHeader(app_name)
            app.link()

    # Delete the tmp folder
    mckp.clean_temp_folder()
