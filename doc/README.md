# Configuration

> 💡 **New to Mackup?** Check out the
> [Architecture Guide](ARCHITECTURE.md) to understand how Mackup works
> under the hood.

All the configuration is done in a file named `.mackup.cfg` stored at the
root of your home folder. This location can be overridden via environment
variables or the `--config-file` command-line option.

To configure Mackup, create a file named `.mackup.cfg` in your home
directory.

```bash
vi ~/.mackup.cfg
```

## Configuration file location

Config files are searched in the following order. If none is found, Mackup will
use the default config location of `~/.mackup.cfg`

- `~/.mackup.cfg`
- `$MACKUP_CONFIG`
- `$XDG_CONFIG_HOME/mackup/mackup.cfg` or `~/.config/mackup/mackup.cfg`

You can also specify a custom config file location using the `--config-file`
command-line option:

```bash
mackup --config-file ~/.mackup-custom.cfg backup
```

The path can be absolute or relative to your home directory. Note that the
config file must be located within your home directory for security reasons.

## Storage

You can specify the storage type Mackup will use to store your configuration
files.

For now, you have 4 options: `dropbox`, `google_drive`, `icloud` and `file_system`.

If none is specified, Mackup will try to use the default: `dropbox`.
With the `dropbox` storage engine, Mackup will automatically figure out your
Dropbox folder.

### Dropbox

```ini
[storage]
engine = dropbox
```

### Google Drive

If you choose the `google_drive` storage engine instead, Mackup will figure out
where your Google Drive is and store your configuration files in it.

```ini
[storage]
engine = google_drive
```

### iCloud

If you choose the `iCloud` storage engine, Mackup will store your
configuration files in the `~/Library/Mobile\ Documents/com\~apple\~CloudDocs/` folder.

```ini
[storage]
engine = icloud
```

You can check if your files are synced using:

```sh
brctl monitor com.apple.CloudDocs
```

### File System

If you want to specify another directory, you can use the `file_system` engine
and Mackup won't try to detect any path for you: it will store your files where
you explicitly told it to, using the `path` setting.
The `path` can be absolute (from the `/` of your drive) or relative to your
home directory.
The `path` setting is mandatory when using the `file_system` engine.

```ini
[storage]
engine = file_system
path = some/folder/in/your/home
# or path = /some/folder/in/your/root
```

Note: you don't need to escape spaces or wrap the path in quotes.
For example, the following paths are valid:

```ini
path = some/path in your/home
path = /some path/in/your/root
```

### Custom Directory Name

You can customize the directory name in which Mackup stores your files. By
default, if not specified, Mackup creates a `Mackup` directory in the storage
engine you chose, e.g. `~/Dropbox/Mackup`.

```ini
[storage]
directory = Mackup
```

For example:

```ini
[storage]
engine = file_system
path = dotfiles
directory = backup
```

This will store your files in the `~/dotfiles/backup` directory in your home.

You can also select a subfolder:

```ini
[storage]
engine = icloud
directory = .config/mackup
```

### Switching Storage

If you ever change your mind and switch storage solutions after Mackup is
already setup (ex: from `dropbox` to `icloud`), complete the following steps.

1. Run `mackup uninstall` on all computers
2. Copy your Mackup files to the new storage location
3. Change the storage provider details in your `.mackup.cfg` file (see above)
4. Run `mackup backup` on the main computer and `mackup restore` on all others

## Applications

### Only sync one or two applications

In your home folder, create a file named `.mackup.cfg` and add the application
names to allow in the `[applications_to_sync]` section, one per line.

```ini
# Example, to only sync SSH and Adium:
[applications_to_sync]
ssh
adium
```

Use `mackup list` to get a list of valid application names. Don't use fancy
names (with spaces) here.

A [sample](.mackup.cfg) of this file is available in this folder. Just copy it
to your home folder:

```bash
cp mackup/doc/.mackup.cfg ~/
```

### Don't sync an application

In your home folder, create a file named `.mackup.cfg` and add the application
names to ignore in the `[applications_to_ignore]` section, one per line.

```ini
# Example, to not sync SSH and Adium:
[applications_to_ignore]
ssh
adium
```

Use `mackup list` to get a list of valid application names. Don't use fancy
names (with spaces) here.

A [sample](.mackup.cfg) of this file is available in this folder. Just copy it
to your home folder:

```bash
cp mackup/doc/.mackup.cfg ~/
```

### Get official support for an application

Open a [new issue](https://github.com/lra/mackup/issues) and ask for it, or
fork Mackup and open a
[Pull Request](https://help.github.com/articles/using-pull-requests).
The stock application configs are in the `mackup/applications` directory.

Remember to follow the guidelines in [CONTRIBUTING.md](https://github.com/lra/mackup/blob/master/.github/CONTRIBUTING.md)
to get your Pull Request merged faster.

### Add support for an application or (almost) any file or directory

You can customize the Mackup engine and add support for unsupported
applications or just custom files and directories you'd like to sync.

NOTE: Files and directories to be synced should be rooted at $HOME.

Let's say that you'd like to add support for Nethack (config file:
`.nethackrc`), for the `bin` and `.hidden` directories and for the
`.gitignore` file you keep in your home.

In your home, create a `.mackup` directory and add a config file for the
application you'd like to support:

```bash
mkdir ~/.mackup
touch ~/.mackup/nethack.cfg
touch ~/.mackup/my-files.cfg
```

Edit those files:

```bash
$ nano ~/.mackup/nethack.cfg
[application]
name = Nethack

[configuration_files]
.nethackrc
```

```bash
$ nano ~/.mackup/my-files.cfg
[application]
name = My personal synced files and dirs

[configuration_files]
bin
.hidden
.gitignore
```

Note that Mackup assumes the file paths listed here are relative to your home
directory.

You can run mackup to see if they are listed:

```bash
$ mackup list
Supported applications:
[...]
 - my-files
 - nethack
[...]
```

All good, you can now sync your newly configured files:

```bash
mackup backup
```

If you override an application config that is already supported by Mackup, your
new config for this application will replace the one provided by Mackup.

You can find some sample configs in this directory.

### Locally test an application before submitting a Pull Request

You can add and test an application by following these steps:

- fork this project
- create a branch _(usually containing the name of the application)_
- add the appropriate application config file in the `mackup/applications` folder
- from the top-most folder _(mackup)_ run `make develop` that replaces the
  currently installed mackup with the local modified one
- simply run `mackup backup` to test if everything is ok
- if everything works as expected:
  - run `make undevelop` to revert to the official version
  - commit and push the change to your fork and then create the Pulls Request

### Add support for an application using the XDG directory

For applications storing their configuration under the `~/.config` folder, you
should not hardcode it. The `.config` folder is the default location but it can
be named differently on other users' systems by setting the `XDG_CONFIG_HOME`
environment variable.

See <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>

Mackup supports this mechanism and provides a dedicated `xdg_configuration_files`
section for those applications.

If any path starts with `.config`, remove the `.config` part and move the path
to a dedicated `xdg_configuration_files` section.

Instead of:

```ini
[application]
name = Git

[configuration_files]
.gitconfig
.config/git/config
.config/git/ignore
.config/git/attributes
```

Use this:

```ini
[application]
name = Git

[configuration_files]
.gitconfig

[xdg_configuration_files]
git/config
git/ignore
git/attributes
```
