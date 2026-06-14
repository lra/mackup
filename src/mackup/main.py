"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2025 Laurent Raufaste <http://glop.org/>

Usage:
  mackup [options] list
  mackup [options] show <application>
  mackup [options] backup [<application>]
  mackup [options] restore [<application>]
  mackup [options] link install [<application>]
  mackup [options] link uninstall [<application>]
  mackup [options] link [<application>]
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
 - mackup show: display the details for a supported application.
 - mackup backup: copy local config files in the configured remote folder.
 - mackup restore: copy config files from the configured remote folder locally.
 - mackup link install: moves local config files in remote folder, and links.
 - mackup link uninstall: removes the links and copy config files locally.
 - mackup link: links local config files from the remote folder.

backup, restore, link install, link uninstall and link act on every configured
application by default. Name a single application (e.g. `mackup backup vim`) to
limit a command to that app, overriding the applications_to_sync and
applications_to_ignore settings in your config.

By default, Mackup syncs all application data via
Dropbox, but may be configured to exclude applications or use a different
backend with a .mackup.cfg file.

See https://github.com/lra/mackup/tree/master/doc for more information.

"""

import sys
from typing import Any

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

    config_file: str | None = args.get("--config-file")
    mckp: Mackup = Mackup(config_file)
    app_db: ApplicationsDatabase = ApplicationsDatabase()

    def print_app_header(app_name: str) -> None:
        if verbose:
            header_str = header("---")
            print(f"\n{header_str} {bold(app_name)} {header_str}")

    def apps_to_process(app_name: str | None) -> set[str]:
        """Resolve which apps a per-app command should act on.

        If an application is named, error out when it is not a supported app
        (like the `show` command) and otherwise act on exactly that app,
        overriding the config's applications_to_sync / applications_to_ignore
        lists. If no application is named, fall back to every configured
        application.
        """
        if app_name:
            if app_name not in app_db.get_app_names():
                sys.exit(f"Unsupported application: {app_name}")
            return {app_name}
        return mckp.get_apps_to_backup()

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
        requested_app_name: str = args["<application>"]

        # Make sure the app exists
        if requested_app_name not in app_db.get_app_names():
            sys.exit(f"Unsupported application: {requested_app_name}")
        print(f"Name: {app_db.get_name(requested_app_name)}")
        print("Configuration files:")
        for file in app_db.get_files(requested_app_name):
            print(f" - {file}")

    # mackup backup [<application>]
    elif args["backup"]:
        # Resolve and validate the target apps before the env check, so an
        # unknown application name fails cleanly without creating the Mackup
        # folder or prompting first.
        app_names = apps_to_process(args["<application>"])
        mckp.check_for_usable_backup_env()

        # Create a backup of the files of each application
        for app_name in sorted(app_names):
            app: ApplicationProfile = ApplicationProfile(
                mckp, app_db.get_files(app_name), dry_run, verbose,
            )
            print_app_header(app_name)
            app.copy_files_to_mackup_folder()

    # mackup restore [<application>]
    elif args["restore"]:
        app_names = apps_to_process(args["<application>"])
        mckp.check_for_usable_restore_env()

        # Recover a backup of the files of each application
        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            print_app_header(app_name)
            app.copy_files_from_mackup_folder()

    # mackup link install [<application>]
    elif args["link"] and args["install"]:
        app_names = apps_to_process(args["<application>"])
        # Check the env where the command is being run
        mckp.check_for_usable_backup_env()

        # Create a link for each application
        for app_name in sorted(app_names):
            app = ApplicationProfile(mckp, app_db.get_files(app_name), dry_run, verbose)
            print_app_header(app_name)
            app.link_install()

    # mackup link uninstall [<application>]
    elif args["link"] and args["uninstall"]:
        # Validate any named application before the env check, so an unknown
        # name fails cleanly before any prompt or side effect.
        named_apps = (
            apps_to_process(args["<application>"]) if args["<application>"] else None
        )

        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if named_apps is not None:
            # Unlink only the named application, leaving the rest of Mackup
            # (and the Mackup config itself) in place. No global confirmation
            # is needed since the user explicitly scoped the uninstall.
            for app_name in sorted(named_apps):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose,
                )
                print_app_header(app_name)
                app.link_uninstall()

        elif dry_run or (
            utils.confirm(
                "You are going to uninstall Mackup.\n"
                "Every configuration file, setting and dotfile"
                " managed by Mackup will be unlinked and copied back"
                " to their original place, in your home folder.\n"
                "Are you sure?",
            )
        ):
            # Uninstall the apps except Mackup, which we'll uninstall last, to
            # keep the settings as long as possible
            app_names = mckp.get_apps_to_backup()
            app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(app_names):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose,
                )
                print_app_header(app_name)
                app.link_uninstall()

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

    # mackup link [<application>]
    elif args["link"]:
        # Validate any named application before the env check.
        named_apps = (
            apps_to_process(args["<application>"]) if args["<application>"] else None
        )

        # Check the env where the command is being run
        mckp.check_for_usable_restore_env()

        if named_apps is not None:
            # Link only the named application. No need to restore the Mackup
            # config first, as the app set is fixed and config-independent here.
            for app_name in sorted(named_apps):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose,
                )
                print_app_header(app_name)
                app.link()
        else:
            # Restore the Mackup config before any other config, as we might
            # need it to know about custom settings
            mackup_app = ApplicationProfile(
                mckp, app_db.get_files(MACKUP_APP_NAME), dry_run, verbose,
            )
            print_app_header(MACKUP_APP_NAME)
            mackup_app.link()

            # Initialize again the apps db, as the Mackup config might have
            # changed it
            mckp = Mackup(config_file)
            app_db = ApplicationsDatabase()

            # Restore the rest of the app configs, using the restored Mackup
            # config
            app_names = mckp.get_apps_to_backup()
            # Mackup has already been done
            app_names.discard(MACKUP_APP_NAME)

            for app_name in sorted(app_names):
                app = ApplicationProfile(
                    mckp, app_db.get_files(app_name), dry_run, verbose,
                )
                print_app_header(app_name)
                app.link()
