"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2021 Laurent Raufaste <http://glop.org/>

Usage:
  mackup list
  mackup [options] backup [<app>...]
  mackup [options] restore [<app>...]
  mackup show <application>
  mackup [options] uninstall [<app>...]
  mackup (-h | --help)
  mackup --version

Options:
  -h --help         Show this screen.
  -c --copy         Copy files rather than symlinking
  -f --force        Force every question asked to be answered with "Yes".
  -r --root         Allow mackup to be run as superuser.
  -n --dry-run      Show steps without executing.
  -v --verbose      Show additional details.
  --version         Show version.

Modes of action:
 1. list: display a list of all supported applications.
 2. backup: sync your conf files to your synced storage, use this the 1st time
    you use Mackup.
 3. restore: link the conf files already in your synced storage on your system,
    use it on any new system you use.
 4. uninstall: reset everything as it was before using Mackup.

By default, Mackup syncs all application data via
Dropbox, but may be configured to exclude applications or use a different
backend with a .mackup.cfg file.

See https://github.com/lra/mackup/tree/master/doc for more information.

"""
import textwrap
from pprint import pprint
from typing import List

from docopt import docopt
from .appsdb import ApplicationsDatabase
from .application import ApplicationProfile
from .colors import warning_log, success_log, magenta, yellow, bold, blue
from .constants import MACKUP_APP_NAME, VERSION
from .mackup import Mackup
from . import utils
import sys


def header(s: str) -> str:
    return blue(s)


def main():
    """Main function."""
    # Get the command line arg
    args = docopt(__doc__, version="Mackup {}".format(VERSION))

    mckp = Mackup()
    app_db = ApplicationsDatabase()

    def printAppHeader(app_name):
        if utils.VERBOSE:
            print(("\n{0} {1} {0}").format(header("---"), bold(app_name)))

    # If we want to answer mackup with "yes" for each question
    if args["--force"]:
        utils.FORCE_YES = True

    # Allow mackup to be run as root
    if args["--root"]:
        utils.CAN_RUN_AS_ROOT = True

    # Copy files into place rather than symlinking them
    if args["--copy"]:
        utils.SHOULD_COPY = True

    if args["--verbose"]:
        utils.VERBOSE = True

    if args["--dry-run"]:
        utils.DRY_RUN = True
        warning_log(magenta("dry-run mode is enabled.  No changes will be made"))

    apps_arg: List[str] = args["<app>"]

    if args["backup"]:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Backup each application
        for app_name in sorted(mckp.get_apps_to_backup(apps_arg)):
            app = ApplicationProfile(app_name, mckp, app_db.get_files(app_name))
            printAppHeader(app_name)
            app.backup()

    elif args["restore"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        # Restore the Mackup config before any other config, as we might need
        # it to know about custom settings
        mackup_app = ApplicationProfile(MACKUP_APP_NAME, mckp, app_db.get_files(MACKUP_APP_NAME))
        printAppHeader(MACKUP_APP_NAME)
        mackup_app.restore()

        # Initialize again the apps db, as the Mackup config might have changed
        mckp = Mackup()
        app_db = ApplicationsDatabase()

        # Restore the rest of the app configs, using the restored Mackup config
        app_names = mckp.get_apps_to_backup(apps_arg)
        # Mackup has already been done
        app_names.discard(MACKUP_APP_NAME)

        for app_name in sorted(app_names):
            app = ApplicationProfile(app_name, mckp, app_db.get_files(app_name))
            printAppHeader(app_name)
            app.restore()

    elif args["uninstall"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if len(apps_arg) == 0:
            msg = """\
                You are going to uninstall Mackup.
                Every configuration file, setting and dotfile managed by Mackup will be unlinked and copied back to their original place, in your home folder.  Are you sure?
            """
        else:
            msg = f"""\
                You are going to uninstall Mackup for these apps: {', '.join(apps_arg)}.
                All configuration files for these apps managed by Mackup will be unlinked/deleted and copied back to their original place, in your home folder.  Are you sure?
            """

        if utils.confirm(yellow(bold(textwrap.dedent(msg)))):
            # Uninstall the apps except Mackup, which we'll uninstall last, to keep the settings as long as possible
            app_names = mckp.get_apps_to_backup(apps_arg)
            app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(app_names):
                app = ApplicationProfile(app_name, mckp, app_db.get_files(app_name))
                printAppHeader(app_name)
                app.uninstall()

            # Restore the Mackup config before any other config, as we might need it to know about custom settings
            mackup_app = ApplicationProfile(MACKUP_APP_NAME, mckp, app_db.get_files(MACKUP_APP_NAME))
            mackup_app.uninstall()

            # Delete the Mackup folder in Dropbox
            # Don't delete this as there might be other Macs that aren't
            # uninstalled yet
            # delete(mckp.mackup_folder)

            success_log(textwrap.dedent(f"""
                All your files have been put back into place. You can now safely uninstall Mackup.
                {bold("Thanks for using Mackup!")}"""))


    elif args["list"]:
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

    # Delete the tmp folder
    mckp.clean_temp_folder()
