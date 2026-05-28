"""
Application Profile.

An Application Profile contains all the information about an application in
Mackup. Name, files, ...
"""

import os
import platform

from . import constants, utils
from .mackup import Mackup


class ApplicationProfile:
    """Instantiate this class with application specific data."""

    def __init__(
        self, mackup: Mackup, files: set[str], dry_run: bool, verbose: bool,
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
        self.files: list[str] = sorted(files)
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

    def _should_use_copy_mode_in_link_workflow(self, filename: str) -> bool:
        """Return whether link commands should fall back to copy mode."""
        if platform.system() != constants.PLATFORM_DARWIN:
            return False

        (home_filepath, _) = self.get_filepaths(filename)
        library_path = os.path.join(os.environ["HOME"], "Library")
        normalized_home_filepath = os.path.normpath(home_filepath)
        normalized_library_path = os.path.normpath(library_path)

        return normalized_home_filepath == normalized_library_path or (
            normalized_home_filepath.startswith(normalized_library_path + os.sep)
        )

    def _copy_file_to_mackup_folder(self, filename: str) -> None:
        """Back up a single application config file to the Mackup folder."""
        (home_filepath, mackup_filepath) = self.get_filepaths(filename)

        if os.path.isfile(home_filepath) or os.path.isdir(home_filepath):
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
                return

            if self.verbose:
                print(
                    f"Backing up\n  {home_filepath}\n  to\n  {mackup_filepath} ...",
                )
            else:
                print(f"Backing up {filename} ...")

            if self.dry_run:
                return

            if os.path.lexists(mackup_filepath):
                file_type: str
                if os.path.isfile(mackup_filepath):
                    file_type = "file"
                elif os.path.isdir(mackup_filepath):
                    file_type = "folder"
                elif os.path.islink(mackup_filepath):
                    file_type = "link"
                else:
                    raise ValueError(f"Unsupported file: {mackup_filepath}")

                if utils.confirm(
                    f"A {file_type} named {mackup_filepath} already exists in the"
                    " Mackup folder.\nAre you sure that you want to"
                    " replace it? (use --force to skip this prompt)",
                ):
                    utils.delete(mackup_filepath)
                else:
                    return

            try:
                utils.copy(home_filepath, mackup_filepath)
            except PermissionError as e:
                print(
                    f"Error: Unable to copy file from {home_filepath} to "
                    f"{mackup_filepath} due to permission issue: {e}",
                )

    def _copy_file_from_mackup_folder(self, filename: str) -> None:
        """Recover a single application config file from the Mackup folder."""
        (home_filepath, mackup_filepath) = self.get_filepaths(filename)

        if os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath):
            if self.verbose:
                print(
                    f"Recovering\n  {mackup_filepath}\n  to\n  {home_filepath} ...",
                )
            else:
                print(f"Recovering {filename} ...")

            if self.dry_run:
                return

            if os.path.lexists(home_filepath):
                if os.path.isfile(home_filepath):
                    file_type = "file"
                elif os.path.isdir(home_filepath):
                    file_type = "folder"
                elif os.path.islink(home_filepath):
                    file_type = "link"
                else:
                    raise ValueError(f"Unsupported file: {home_filepath}")

                if utils.confirm(
                    f"A {file_type} named {home_filepath} already exists in your"
                    " home folder.\nAre you sure that you want to"
                    " replace it?",
                ):
                    utils.delete(home_filepath)
                else:
                    return

            try:
                utils.copy(mackup_filepath, home_filepath)
            except PermissionError as e:
                print(
                    f"Error: Unable to copy file from {mackup_filepath} to "
                    f"{home_filepath} due to permission issue: {e}",
                )

    def _link_install_file(self, filename: str) -> None:
        """Create a single application config file link."""
        (home_filepath, mackup_filepath) = self.get_filepaths(filename)

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
                return

            if os.path.exists(mackup_filepath):
                if os.path.isfile(mackup_filepath):
                    file_type = "file"
                elif os.path.isdir(mackup_filepath):
                    file_type = "folder"
                elif os.path.islink(mackup_filepath):
                    file_type = "link"
                else:
                    raise ValueError(f"Unsupported file: {mackup_filepath}")

                if utils.confirm(
                    f"A {file_type} named {mackup_filepath} already exists in the"
                    " backup.\nAre you sure that you want to"
                    " replace it?",
                ):
                    utils.delete(mackup_filepath)
                    utils.copy(home_filepath, mackup_filepath)
                    utils.delete(home_filepath)
                    utils.link(mackup_filepath, home_filepath)
            else:
                utils.copy(home_filepath, mackup_filepath)
                utils.delete(home_filepath)
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

    def _link_file(self, filename: str) -> None:
        """Link a single application config file from Mackup to home."""
        (home_filepath, mackup_filepath) = self.get_filepaths(filename)

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
                return

            if os.path.exists(home_filepath):
                if os.path.isfile(home_filepath):
                    file_type = "file"
                elif os.path.isdir(home_filepath):
                    file_type = "folder"
                elif os.path.islink(home_filepath):
                    file_type = "link"
                else:
                    raise ValueError(f"Unsupported file: {home_filepath}")

                if utils.confirm(
                    f"You already have a {file_type} at {home_filepath}.\n"
                    "Do you want to replace it with your backup?",
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
                print(f"Doing nothing\n  {mackup_filepath}\n  does not exist")

    def _link_uninstall_file(self, filename: str) -> None:
        """Revert a single symlinked application config file back to a copy."""
        (home_filepath, mackup_filepath) = self.get_filepaths(filename)

        if os.path.isfile(mackup_filepath) or os.path.isdir(mackup_filepath):
            if os.path.exists(home_filepath):
                if not os.path.islink(home_filepath) or not os.path.samefile(
                    home_filepath, mackup_filepath,
                ):
                    print(
                        f'Warning: the file in your home "{home_filepath}" '
                        f"does not point to the original file in Mackup "
                        f"{mackup_filepath}, skipping...",
                    )
                    return

                if self.verbose:
                    print(f"Reverting {mackup_filepath}\n at {home_filepath} ...")
                else:
                    print(f"Reverting {filename} ...")

                if self.dry_run:
                    return

                utils.delete(home_filepath)
                utils.copy(mackup_filepath, home_filepath)
        elif self.verbose:
            print(f"Doing nothing, {mackup_filepath} does not exist")

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
            self._copy_file_to_mackup_folder(filename)

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
            self._copy_file_from_mackup_folder(filename)

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
        for filename in self.files:
            if self._should_use_copy_mode_in_link_workflow(filename):
                self._copy_file_to_mackup_folder(filename)
            else:
                self._link_install_file(filename)

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
        for filename in self.files:
            if self._should_use_copy_mode_in_link_workflow(filename):
                self._copy_file_from_mackup_folder(filename)
            else:
                self._link_file(filename)

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
        for filename in self.files:
            if self._should_use_copy_mode_in_link_workflow(filename):
                self._copy_file_from_mackup_folder(filename)
            else:
                self._link_uninstall_file(filename)
