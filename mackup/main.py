"""Mackup.

Keep your application settings in sync.
Copyright (C) 2013-2015 Laurent Raufaste <http://glop.org/>

Usage:
  mackup [options] list
  mackup [options] backup
  mackup [options] restore
  mackup [options] uninstall
  mackup [options] show <app>
  mackup (-h | --help)
  mackup --version

Options:
  -h --help     Show this screen.
  -f --force    Force every question asked to be answered with "Yes".
  -n --dry-run  Show steps without executing.
  -v --verbose  Show additional details.
  -d --debug    Debug mode.
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
import logging
logging.basicConfig(level=logging.WARN)


from docopt import docopt
from .constants import MACKUP_APP_NAME, VERSION
from .mackup import Mackup
from . import utils


def main():
    """
    Protect the main function from Ctrl+C. Here we can also handle controlled
    exceptions if any...
    """
    try:
        _main()
    except KeyboardInterrupt:
        print("\n\nAborted by the user... exiting\n")


def _main():
    """Main function."""
    # Get the command line arg
    args = docopt(__doc__, version="Mackup {}".format(VERSION))
    logging.info("Running with args: %s" % str(args))

    # If we want to answer mackup with "yes" for each question
    if args['--force']:
        utils.FORCE_YES = True

    if args['--debug']:
        logging.getLogger().setLevel(logging.DEBUG)

    mckp = Mackup()
    mckp.dry_run = args['--dry-run']
    mckp.verbose = args['--verbose']

    if args['backup']:
        mckp.backup()
    elif args['restore']:
        mckp.restore()
    elif args['uninstall']:
        mckp.uninstall()
    elif args['list']:
        mckp.list()
    elif args['show']:
        print("\nConfig found in '%s':\n\n%s" %
              mckp.app_db.get_config(args['<app>']))

    # Delete the tmp folder
    mckp.clean_temp_folder()
