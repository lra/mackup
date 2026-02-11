"""
Application Profile.

An Application Profile contains all the information about an application in
Mackup. Name, files, ...
"""

import os

from . import utils
from .mackup import Mackup


class ApplicationProfile:
    """Instantiate this class with application specific data."""

    def __init__(
        self, mackup: Mackup, files: set[str], dry_run: bool, verbose: bool
    ) -> None:
        """
        Create an ApplicationProfile instance.

        Args:
            mackup (Mackup)
            files (list)
        """
        assert isinstance(mackup, Mackup)
        assert isinstance(files, set)

        self.mackup: Mackup = mackup
        self.files: list[str] = list(files)
        self.dry_run: bool = dry_run
        self.verbose: bool = verbose

    def get_filepaths(self, filename: str) -> tuple[str, str]:
        """
        Get home and mackup filepaths for given file

        Args:
            filename (str)

        Returns:
            home_filepath, mackup_filepath (str, str)
        """
        return (
            os.path.join(os.environ["HOME"], filename),
            os.path.join(self.mackup.mackup_folder, filename),
        )

    def copy_files_to_mackup_folder(self) -> None:
        """
        Backup the application config files to the Mackup folder.

        Algorithm:
            for config_file
                if config_file exists and is a real file/folder
                    if home/file is a symlink pointing to mackup/file
                        skip (already backed up via link install)
                    if exists mackup/file
                        are you sure?
                        if sure
                            rm mackup/file
                    cp home/file mackup/file
        """
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.get_filepaths(filename)

            # If config_file exists and is a real file/folder
            if (os.path.isfile(home_filepath) or os.path.isdir(home_filepath)):
                # Check if home file is a symlink pointing to mackup file
                # (already backed up via link install)
                if (
                    os.path.islink(home_filepath)
                    and os.path.exists(mackup_filepath)
                    and os.path.samefile(home_filepath, mackup_filepath)
                ):
                    if self.verbose:
                        print(
                            f"Skipping {home_filepath}\n"
                            f"  already linked to\n  {mackup_filepath}",
                        )
                    continue

                if self.verbose:
                    print(
                        f"Backing up\n  {home_filepath}\n  to\n  {mackup_filepath} ...",
                    )
                else:
                    print(f"Backing up {filename} ...")

                if self.dry_run:
                    continue

                # If exists mackup/file
                if os.path.lexists(mackup_filepath):
                    # Name it right
                    file_type: str
                    if os.path.isfile(mackup_filepath):
                        file_type = "file"
                    elif os.path.isdir(mackup_filepath):
                        file_type = "folder"
                    elif os.path.islink(mackup_filepath):
                        file_type = "link"
                    else:
                        raise ValueError(f"Unsupported file: {mackup_filepath}")
                    # Ask the user if he really wants to replace it
                    if utils.confirm(
                        f"A {file_type} named {mackup_filepath} already exists in the"
                        " Mackup folder.\nAre you sure that you want to"
                        " replace it? (use --force to skip this prompt)",
                    ):
                        # If confirmed, delete the file in Mackup
                        utils.delete(mackup_filepath)

                # Copy the file
                try:
                    utils.copy(home_filepath, mackup_filepath)
                except PermissionError as e:
                    print(
                        f"Error: Unable to copy file from {home_filepath} to "
                        f"{mackup_filepath} due to permission issue: {e}"
                    )

    def copy_files_from_mackup_folder(self) -> None:
        """
        Recover the application config files from the Mackup folder.

        Algorithm:
            for config_file
                if config_file exists in mackup and is a real file/folder
                    if exists home/file
                        are you sure?
                        if sure
                            rm home/file
                    cp mackup/file home/file
        """
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.get_filepaths(filename)

            # If config_file exists in mackup and is a real file/folder
            if (os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath)):
                if self.verbose:
                    print(
                        f"Recovering\n  {mackup_filepath}\n  to\n  {home_filepath} ...",
                    )
                else:
                    print(f"Recovering {filename} ...")

                if self.dry_run:
                    continue

                # If exists home/file
                if os.path.lexists(home_filepath):
                    # Name it right
                    if os.path.isfile(home_filepath):
                        file_type = "file"
                    elif os.path.isdir(home_filepath):
                        file_type = "folder"
                    elif os.path.islink(home_filepath):
                        file_type = "link"
                    else:
                        raise ValueError(f"Unsupported file: {home_filepath}")
                    # Ask the user if he really wants to replace it
                    if utils.confirm(
                        f"A {file_type} named {home_filepath} already exists in your"
                        " home folder.\nAre you sure that you want to"
                        " replace it?",
                    ):
                        # If confirmed, delete the file in Mackup
                        utils.delete(home_filepath)

                # Copy the file
                try:
                    utils.copy(mackup_filepath, home_filepath)
                except PermissionError as e:
                    print(
                        f"Error: Unable to copy file from {mackup_filepath} to "
                        f"{home_filepath} due to permission issue: {e}"
                    )

    def link_install(self) -> None:
        """
        Create the application config file links.

        Algorithm:
            if exists home/file
              if home/file is a real file
                if exists mackup/file
                  are you sure?
                  if sure
                    rm mackup/file
                    mv home/file mackup/file
                    link mackup/file home/file
                else
                  mv home/file mackup/file
                  link mackup/file home/file
        """
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.get_filepaths(filename)

            # If the file exists and is not already a link pointing to Mackup
            if (os.path.isfile(home_filepath) or os.path.isdir(home_filepath)) and not (
                os.path.islink(home_filepath)
                and (os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath))
                and os.path.samefile(home_filepath, mackup_filepath)
            ):
                if self.verbose:
                    print(
                        f"Backing up\n  {home_filepath}\n  to\n  {mackup_filepath} ...",
                    )
                else:
                    print(f"Linking {filename} ...")

                if self.dry_run:
                    continue

                # Check if we already have a backup
                if os.path.exists(mackup_filepath):
                    # Name it right
                    if os.path.isfile(mackup_filepath):
                        file_type = "file"
                    elif os.path.isdir(mackup_filepath):
                        file_type = "folder"
                    elif os.path.islink(mackup_filepath):
                        file_type = "link"
                    else:
                        raise ValueError(f"Unsupported file: {mackup_filepath}")

                    # Ask the user if he really wants to replace it
                    if utils.confirm(
                        f"A {file_type} named {mackup_filepath} already exists in the"
                        " backup.\nAre you sure that you want to"
                        " replace it?",
                    ):
                        # Delete the file in Mackup
                        utils.delete(mackup_filepath)
                        # Copy the file
                        utils.copy(home_filepath, mackup_filepath)
                        # Delete the file in the home
                        utils.delete(home_filepath)
                        # Link the backuped file to its original place
                        utils.link(mackup_filepath, home_filepath)
                else:
                    # Copy the file
                    utils.copy(home_filepath, mackup_filepath)
                    # Delete the file in the home
                    utils.delete(home_filepath)
                    # Link the backuped file to its original place
                    utils.link(mackup_filepath, home_filepath)
            elif self.verbose:
                if os.path.exists(home_filepath):
                    print(
                        f"Doing nothing\n  {home_filepath}\n  "
                        f"is already backed up to\n  {mackup_filepath}",
                    )
                elif os.path.islink(home_filepath):
                    print(
                        f"Doing nothing\n  {home_filepath}\n  "
                        "is a broken link, you might want to fix it.",
                    )
                else:
                    print(f"Doing nothing\n  {home_filepath}\n  does not exist")

    def link(self) -> None:
        """
        Link the application config files.

        Algorithm:
            if exists mackup/file
              if exists home/file
                are you sure?
                if sure
                  rm home/file
                  link mackup/file home/file
              else
                link mackup/file home/file
        """
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.get_filepaths(filename)

            # If the file exists and is not already pointing to the mackup file
            # and the folder makes sense on the current platform (Don't sync
            # any subfolder of ~/Library on GNU/Linux)
            file_or_dir_exists: bool = os.path.isfile(mackup_filepath) or os.path.isdir(
                mackup_filepath,
            )
            pointing_to_mackup: bool = (
                os.path.islink(home_filepath)
                and os.path.exists(mackup_filepath)
                and os.path.samefile(mackup_filepath, home_filepath)
            )
            supported: bool = utils.can_file_be_synced_on_current_platform(filename)

            if file_or_dir_exists and not pointing_to_mackup and supported:
                if self.verbose:
                    print(
                        f"Restoring\n  linking {home_filepath}\n"
                        f"  to      {mackup_filepath} ...",
                    )
                else:
                    print(f"Restoring {filename} ...")

                if self.dry_run:
                    continue

                # Check if there is already a file in the home folder
                if os.path.exists(home_filepath):
                    # Name it right
                    if os.path.isfile(home_filepath):
                        file_type = "file"
                    elif os.path.isdir(home_filepath):
                        file_type = "folder"
                    elif os.path.islink(home_filepath):
                        file_type = "link"
                    else:
                        raise ValueError(f"Unsupported file: {mackup_filepath}")

                    if utils.confirm(
                        f"You already have a {file_type} named {filename} in your"
                        " home.\nDo you want to replace it with"
                        " your backup?",
                    ):
                        utils.delete(home_filepath)
                        utils.link(mackup_filepath, home_filepath)
                else:
                    utils.link(mackup_filepath, home_filepath)
            elif self.verbose:
                if os.path.exists(home_filepath):
                    print(
                        f"Doing nothing\n  {mackup_filepath}\n"
                        f"  already linked by\n  {home_filepath}",
                    )
                elif os.path.islink(home_filepath):
                    print(
                        f"Doing nothing\n  {home_filepath}\n  "
                        "is a broken link, you might want to fix it.",
                    )
                else:
                    print(
                        f"Doing nothing\n  {mackup_filepath}\n  does not exist",
                    )

    def link_uninstall(self) -> None:
        """
        Removes links and copy config files from the remote folder locally.

        Algorithm:
            for each file in config
                if mackup/file exists
                    if home/file exists
                        delete home/file
                    copy mackup/file home/file
        """
        # For each file used by the application
        for filename in self.files:
            (home_filepath, mackup_filepath) = self.get_filepaths(filename)

            # If the mackup file exists
            if os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath):
                # Check if there is a corresponding file in the home folder
                if os.path.exists(home_filepath):
                    # If the home file is not a link or does not point to the
                    # mackup file, display a warning and skip it.
                    if not os.path.islink(home_filepath) or not os.path.samefile(
                        home_filepath, mackup_filepath
                    ):
                        print(
                            f'Warning: the file in your home "{home_filepath}" '
                            f"does not point to the original file in Mackup "
                            f"{mackup_filepath}, skipping..."
                        )
                        continue
                    if self.verbose:
                        print(
                            f"Reverting {mackup_filepath}\n at {home_filepath} ...",
                        )
                    else:
                        print(f"Reverting {filename} ...")

                    if self.dry_run:
                        continue

                    # If there is, delete it as we are gonna copy the Dropbox
                    # one there
                    utils.delete(home_filepath)

                    # Copy the Dropbox file to the home folder
                    utils.copy(mackup_filepath, home_filepath)
            elif self.verbose:
                print(f"Doing nothing, {mackup_filepath} does not exist")
