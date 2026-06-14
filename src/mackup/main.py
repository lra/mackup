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
from dataclasses import dataclass
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


@dataclass
class _Context:
    """Shared state threaded through the command handlers."""

    config_file: str | None
    mckp: Mackup
    app_db: ApplicationsDatabase
    dry_run: bool
    verbose: bool


def _print_app_header(app_name: str, verbose: bool) -> None:
    if verbose:
        header_str = header("---")
        print(f"\n{header_str} {bold(app_name)} {header_str}")


def _resolve_apps(app_name: str | None, ctx: _Context) -> set[str]:
    """Resolve which apps a per-app command should act on.

    If an application is named, error out when it is not a supported app
    (like the `show` command) and otherwise act on exactly that app,
    overriding the config's applications_to_sync / applications_to_ignore
    lists. If no application is named, fall back to every configured
    application.
    """
    if app_name:
        if app_name not in ctx.app_db.get_app_names():
            sys.exit(f"Unsupported application: {app_name}")
        return {app_name}
    return ctx.mckp.get_apps_to_backup()


def _run_action(ctx: _Context, app_names: set[str], action: str) -> None:
    """Run an ApplicationProfile method over each app, in sorted order."""
    for app_name in sorted(app_names):
        app = ApplicationProfile(
            ctx.mckp, ctx.app_db.get_files(app_name), ctx.dry_run, ctx.verbose,
        )
        _print_app_header(app_name, ctx.verbose)
        getattr(app, action)()


def _cmd_list(app_db: ApplicationsDatabase) -> None:
    output: str = "Supported applications:\n"
    for app_name in sorted(app_db.get_app_names()):
        output += f" - {app_name}\n"
    output += "\n"
    output += (
        f"{len(app_db.get_app_names())} applications supported in Mackup v{VERSION}"
    )
    print(output)


def _cmd_show(args: dict[str, Any], app_db: ApplicationsDatabase) -> None:
    requested_app_name: str = args["<application>"]

    # Make sure the app exists
    if requested_app_name not in app_db.get_app_names():
        sys.exit(f"Unsupported application: {requested_app_name}")
    print(f"Name: {app_db.get_name(requested_app_name)}")
    print("Configuration files:")
    for file in app_db.get_files(requested_app_name):
        print(f" - {file}")


def _cmd_backup(args: dict[str, Any], ctx: _Context) -> None:
    # Resolve and validate the target apps before the env check, so an
    # unknown application name fails cleanly without creating the Mackup
    # folder or prompting first.
    app_names = _resolve_apps(args["<application>"], ctx)
    ctx.mckp.check_for_usable_backup_env()

    # Create a backup of the files of each application
    _run_action(ctx, app_names, "copy_files_to_mackup_folder")


def _cmd_restore(args: dict[str, Any], ctx: _Context) -> None:
    app_names = _resolve_apps(args["<application>"], ctx)
    ctx.mckp.check_for_usable_restore_env()

    # Recover a backup of the files of each application
    _run_action(ctx, app_names, "copy_files_from_mackup_folder")


def _cmd_link_install(args: dict[str, Any], ctx: _Context) -> None:
    app_names = _resolve_apps(args["<application>"], ctx)
    # Check the env where the command is being run
    ctx.mckp.check_for_usable_backup_env()

    # Create a link for each application
    _run_action(ctx, app_names, "link_install")


def _cmd_link_uninstall(args: dict[str, Any], ctx: _Context) -> None:
    # Validate any named application before the env check, so an unknown
    # name fails cleanly before any prompt or side effect.
    named_apps = (
        _resolve_apps(args["<application>"], ctx) if args["<application>"] else None
    )

    # Check the env where the command is being run
    ctx.mckp.check_for_usable_restore_env()

    if named_apps is not None:
        # Unlink only the named application, leaving the rest of Mackup
        # (and the Mackup config itself) in place. No global confirmation
        # is needed since the user explicitly scoped the uninstall.
        _run_action(ctx, named_apps, "link_uninstall")

    elif ctx.dry_run or (
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
        app_names = ctx.mckp.get_apps_to_backup()
        app_names.discard(MACKUP_APP_NAME)

        _run_action(ctx, app_names, "link_uninstall")

        # Restore the Mackup config before any other config, as we might
        # need it to know about custom settings
        mackup_app = ApplicationProfile(
            ctx.mckp, ctx.app_db.get_files(MACKUP_APP_NAME), ctx.dry_run, ctx.verbose,
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


def _cmd_link(args: dict[str, Any], ctx: _Context) -> None:
    # Validate any named application before the env check.
    named_apps = (
        _resolve_apps(args["<application>"], ctx) if args["<application>"] else None
    )

    # Check the env where the command is being run
    ctx.mckp.check_for_usable_restore_env()

    if named_apps is not None:
        # Link only the named application. No need to restore the Mackup
        # config first, as the app set is fixed and config-independent here.
        _run_action(ctx, named_apps, "link")
        return

    # Restore the Mackup config before any other config, as we might
    # need it to know about custom settings
    mackup_app = ApplicationProfile(
        ctx.mckp, ctx.app_db.get_files(MACKUP_APP_NAME), ctx.dry_run, ctx.verbose,
    )
    _print_app_header(MACKUP_APP_NAME, ctx.verbose)
    mackup_app.link()

    # Initialize again the apps db, as the Mackup config might have
    # changed it
    ctx.mckp = Mackup(ctx.config_file)
    ctx.app_db = ApplicationsDatabase()

    # Restore the rest of the app configs, using the restored Mackup config
    app_names = ctx.mckp.get_apps_to_backup()
    # Mackup has already been done
    app_names.discard(MACKUP_APP_NAME)

    _run_action(ctx, app_names, "link")


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
    ctx = _Context(
        config_file=config_file,
        mckp=Mackup(config_file),
        app_db=ApplicationsDatabase(),
        dry_run=args["--dry-run"],
        verbose=args["--verbose"],
    )

    # If we want to answer mackup with "yes" for each question
    if args["--force"]:
        utils.FORCE_YES = True

    # If we want to answer mackup with "no" for each question
    if args["--force-no"]:
        utils.FORCE_NO = True

    # Allow mackup to be run as root
    if args["--root"]:
        utils.CAN_RUN_AS_ROOT = True

    if args["list"]:
        ctx.mckp.check_for_usable_environment()
        _cmd_list(ctx.app_db)
    elif args["show"]:
        ctx.mckp.check_for_usable_environment()
        _cmd_show(args, ctx.app_db)
    elif args["backup"]:
        _cmd_backup(args, ctx)
    elif args["restore"]:
        _cmd_restore(args, ctx)
    elif args["link"] and args["install"]:
        _cmd_link_install(args, ctx)
    elif args["link"] and args["uninstall"]:
        _cmd_link_uninstall(args, ctx)
    elif args["link"]:
        _cmd_link(args, ctx)
