"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2025 Laurent Raufaste <http://glop.org/>

Usage:
  mackup [options] list
  mackup [options] show [<application>...]
  mackup [options] backup [--all | <app>...]
  mackup [options] restore [--all | <app>...]
  mackup [options] link install [--all | <app>...]
  mackup [options] link [--all | <app>...]
  mackup [options] link uninstall [--all | <app>...]
  mackup (-h | --help)

Options:
  -h --help                 Show this screen.
  -f --force                Force every question asked to be answered with "Yes".
  --force-no                Force every question asked to be answered with "No".
  -r --root                 Allow mackup to be run as superuser.
  -n --dry-run              Show steps without executing.
  -v --verbose              Show additional details.
  -c --config-file=<path>   Specify custom config file path.
  --version                 Show version.

Modes of action:
 - mackup list: display a list of all supported applications.
 - mackup show: display the details for one or more supported applications.
 - mackup backup: copy local config files in the configured remote folder.
 - mackup restore: copy config files from the configured remote folder locally.
 - mackup link install: moves local config files in remote folder, and links.
 - mackup link: links local config files from the remote folder.
 - mackup link uninstall: removes the links and copy config files locally.

By default, Mackup syncs all application data via
Dropbox, but may be configured to exclude applications or use a different
backend with a .mackup.cfg file.

See https://github.com/lra/mackup/tree/master/doc for more information.

"""

import sys
from typing import Any, Optional

from docopt import docopt

from . import utils
from .application import ApplicationProfile
from .appsdb import ApplicationsDatabase
from .constants import MACKUP_APP_NAME, VERSION
from .mackup import Mackup


class ColorFormatCodes:
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    NORMAL = "\033[0m"


def header(text: str) -> str:
    return ColorFormatCodes.BLUE + text + ColorFormatCodes.NORMAL


def bold(text: str) -> str:
    return ColorFormatCodes.BOLD + text + ColorFormatCodes.NORMAL


def validate_app_names(
    requested_apps: set[str], available_apps: set[str], command: str = "",
) -> set[str]:
    """Validate requested app names against available apps.

    Args:
        requested_apps: Set of app names requested by user
        available_apps: Set of valid app names from database
        command: Name of the command (for error messages)

    Returns:
        Set of valid app names

    Raises:
        SystemExit: If any requested app is not found
    """
    invalid_apps = requested_apps - available_apps
    if invalid_apps:
        invalid_list = ", ".join(sorted(invalid_apps))
        sys.exit(f"Unsupported application(s): {invalid_list}")
    return requested_apps & available_apps


def main() -> None:
    """Main function."""
    # Get the command line arg
    docstring = __doc__
    if not docstring:
        sys.exit(
            "Usage information is not available because __doc__ is None. "
            "This can happen when running Python with optimizations (python -OO). "
            "Please run Mackup without -OO to use the command-line interface.",
        )
    assert docstring is not None  # for type narrowing after sys.exit

    args: dict[str, Any] = docopt(docstring, version=f"Mackup {VERSION}")

    if args["--force"] and args["--force-no"]:
        sys.exit("Options --force and --force-no are mutually exclusive.")

    config_file: Optional[str] = args.get("--config-file")
    mckp: Mackup = Mackup(config_file)
    app_db: ApplicationsDatabase = ApplicationsDatabase()

    def print_app_header(app_name: str) -> None:
        if verbose:
            header_str = header("---")
            print(f"\n{header_str} {bold(app_name)} {header_str}")

    # If we want to answer mackup with "yes" for each question
    if args["--force"]:
        utils.FORCE_YES = True

    # If we want to answer mackup with "no" for each question
    if args["--force-no"]:
        utils.FORCE_NO = True

    # Allow mackup to be run as root
    if args["--root"]:
        utils.CAN_RUN_AS_ROOT = True

    dry_run: bool = args["--dry-run"]

    verbose: bool = args["--verbose"]

    # mackup list
    if args["list"]:
        # Display the list of supported applications
        mckp.check_for_usable_environment()
        output: str = "Supported applications:\n"
        for app_name in sorted(app_db.get_app_names()):
            output += f" - {app_name}\n"
        output += "\n"
        output += (
            f"{len(app_db.get_app_names())} applications supported in "
            f"Mackup v{VERSION}"
        )
        print(output)

    # mackup show <application>
    elif args["show"]:
        mckp.check_for_usable_environment()
        requested_apps: list[str] = args["<application>"]

        if not requested_apps:
            # Show all applications
            sys.exit("Please specify at least one application to show.")

        # Validate all requested apps
        available_apps: set[str] = app_db.get_app_names()
        requested_app_set = set(requested_apps)
        validate_app_names(requested_app_set, available_apps, "show")

        # Show details for each requested app
        for app_name in sorted(requested_app_set):
            print(f"Name: {app_db.get_name(app_name)}")
            print("Configuration files:")
            for file in app_db.get_files(app_name):
                print(f" - {file}")
            print()

    # mackup backup
    elif args["backup"]:
        mckp.check_for_usable_backup_env()

        app_names = set(args["<app>"]) if args["<app>"] else mckp.get_apps_to_backup()

        # Validate app names if explicitly provided
        if args["<app>"]:
            available_apps: set[str] = app_db.get_app_names()
            app_names = validate_app_names(app_names, available_apps, "backup")

        # Create a backup of the files of each application
        for app_name in sorted(app_names):
            app: ApplicationProfile = ApplicationProfile(
                mckp, app_db.get_files(app_name), dry_run, verbose,
            )
            print_app_header(app_name)
            app.copy_files_to_mackup_folder()

    # mackup restore
    elif args["restore"]:
        mckp.check_for_usable_restore_env()

        app_names = set(args["<app>"]) if args["<app>"] else mckp.get_apps_to_backup()

        # Validate app names if explicitly provided
        if args["<app>"]:
            available_apps: set[str] = app_db.get_app_names()
            app_names = validate_app_names(app_names, available_apps, "restore")

        # Recover a backup of the files of each application
        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            print_app_header(app_name)
            app.copy_files_from_mackup_folder()

    # mackup link install
    elif args["link"] and args["install"]:
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        app_names = set(args["<app>"]) if args["<app>"] else mckp.get_apps_to_backup()

        # Validate app names if explicitly provided
        if args["<app>"]:
            available_apps: set[str] = app_db.get_app_names()
            app_names = validate_app_names(app_names, available_apps, "link install")

        # Create a link for each application
        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            print_app_header(app_name)
            app.link_install()

    # mackup link uninstall
    elif args["link"] and args["uninstall"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        app_names = set(args["<app>"]) if args["<app>"] else mckp.get_apps_to_backup()

        # Validate app names if explicitly provided
        if args["<app>"]:
            available_apps: set[str] = app_db.get_app_names()
            app_names = validate_app_names(app_names, available_apps, "link uninstall")

        if dry_run or (
            utils.confirm(
                "You are going to unlink Mackup managed configuration files.\n"
                "Are you sure?",
            )
        ):
            # Uninstall the apps except Mackup, which we'll uninstall last, to
            # keep the settings as long as possible
            if not args["<app>"] and MACKUP_APP_NAME in app_names:
                app_names.discard(MACKUP_APP_NAME)
                uninstall_mackup_app = True
            else:
                uninstall_mackup_app = False

            for app_name in sorted(app_names):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose,
                )
                print_app_header(app_name)
                app.link_uninstall()

            if uninstall_mackup_app:
                # Restore the Mackup config before any other config, as we might
                # need it to know about custom settings
                mackup_app = ApplicationProfile(
                    mckp, app_db.get_files(MACKUP_APP_NAME), dry_run, verbose,
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
                    "Thanks for using Mackup!",
                )

    # mackup link
    elif args["link"]:
        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if args["<app>"]:
            app_names = set(args["<app>"])
            # Validate app names if explicitly provided
            available_apps: set[str] = app_db.get_app_names()
            app_names = validate_app_names(app_names, available_apps, "link")
        else:
            # Restore the Mackup config before any other config, as we might need
            # it to know about custom settings
            mackup_app = ApplicationProfile(
                mckp, app_db.get_files(MACKUP_APP_NAME), dry_run, verbose,
            )
            print_app_header(MACKUP_APP_NAME)
            mackup_app.link()

            # Initialize again the apps db, as the Mackup config might have changed
            # it
            mckp = Mackup(config_file)
            app_db = ApplicationsDatabase()

            # Restore the rest of the app configs, using the restored Mackup config
            app_names = mckp.get_apps_to_backup()
            # Mackup has already been done
            app_names.discard(MACKUP_APP_NAME)

        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            print_app_header(app_name)
            app.link()

    # Delete the tmp folder
    mckp.clean_temp_folder()
