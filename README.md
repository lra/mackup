# Mackup

Keep your application settings in sync.

[![Circle CI](https://circleci.com/gh/lra/mackup.svg?style=shield)](https://circleci.com/gh/lra/mackup)
[![snapcraft](https://snapcraft.io/mackup/badge.svg)](https://snapcraft.io/mackup)

## Table of content

- [Quickstart](#quickstart)
- [Usage](#usage)
- [What does it do](#what-does-it-do)
- [Bullsh\*t, what does it really do to my files](#bullsht-what-does-it-really-do-to-my-files)
- [Supported Storages](#supported-storages)
- [Supported Applications](#supported-applications)
- [Can you support application X](#can-you-support-application-x)
- [Why did you do this](#why-did-you-do-this)
- [What platforms are supported](#what-platforms-are-supported)
- [What's up with the weird name](#whats-up-with-the-weird-name)
- [Where can I find more information](#where-can-i-find-more-information)

## Quickstart

If you have [Dropbox](https://www.dropbox.com) installed and want to use it to
save your config files, that's super easy.

On OS X, if you want an easy install, you can install
[Homebrew](http://brew.sh/) and do:

```bash
# Install Mackup
brew install mackup

# Launch it and back up your files
mackup backup
```

If not running OS X, or you don't like Homebrew, you can use [pip](https://pip.pypa.io/en/stable/).

> Note: The below command will check if a previous version of Mackup
> is already installed on your system.
> If this is the case, it will be upgraded to the latest version.

```bash
# Install Mackup with PIP
pip install --upgrade mackup

# Launch it and back up your files
mackup backup
```

> On **Ubuntu**, pip will install to the current user's home
> directory rather than system-wide. Because of this, when
> installing pip on **Ubuntu** you will need to run `pip install`
> with the `--system` flag as well (on other platforms this is not
> needed)

You're all set and constantly backed up from now on.

Next, on any new workstation, do:

```bash
# Install Mackup
brew install mackup

# Launch it and restore your files
mackup restore
```

Done!

You can find more detailed instructions in [INSTALL.md](INSTALL.md).

## Usage

`mackup backup`

Backup your application settings.

`mackup restore`

Restore your application settings on a newly installed workstation.

`mackup uninstall`

Copy back any synced config file to its original place.

`mackup list`

Display the list of applications supported by Mackup.

`mackup -h`

Get some help, obviously...

## What does it do

- Back ups your application settings in a safe directory (e.g. Dropbox)
- Syncs your application settings among all your workstations
- Restores your configuration on any fresh install in one command line

By only tracking pure configuration files, it keeps the crap out of your
freshly new installed workstation (no cache, temporary and locally specific
files are transfered).

Mackup makes setting up the environment easy and simple, saving time for your
family, great ideas, and all the cool stuff you like.

## Bullsh\*t, what does it really do to my files

Let's take `git` as an example. Your settings for `git` are saved in your home
folder, in the `.gitconfig` file.

### Backup

If you have Dropbox, these things happen when you launch `mackup backup`:

1. `cp ~/.gitconfig ~/Dropbox/Mackup/.gitconfig`
1. `rm ~/.gitconfig`
1. `ln -s ~/Dropbox/Mackup/.gitconfig ~/.gitconfig`

Now your `git` config is always backed up and up to date on all your workstations.

### Restore

When you launch `mackup restore`, here's what it's really doing:

1. `ln -s ~/Dropbox/Mackup/.gitconfig ~/.gitconfig`

That's it, you got your `git` config setup on your new workstation.

`mackup` does the same for any supported application.

### Uninstall

You can revert all your files to their original state.

```bash
# Just run this
mackup uninstall
```

This will remove the symlinks and copy back the files from the Mackup folder in
Dropbox to their original places in your home. The Mackup folder and the files
in it stay put, so that any other computer also running Mackup is unaffected.

## Supported Storages

- [Dropbox](https://www.dropbox.com/)
- [Google Drive](https://drive.google.com/)
- [Copy](https://www.copy.com/)
- [iCloud](http://www.apple.com/icloud/)
- [Box](https://www.box.com)
- Anything able to sync a folder (e.g. [Git](http://git-scm.com/))

See the [README](doc/README.md) file in the doc directory for more info.

## Supported Applications

See the currently [supported Applications](SUPPORTED_APPLICATIONS.md).

## Can you support application X

We can [with your help](doc#get-official-support-for-an-application) ;)

## Personalization & configuration

Have an application that shouldn't be generally supported but that you use?
Or a cool file you want to sync?

- Create a `~/.mackup` directory to [sync an application or any file or directory](doc#add-support-for-an-application-or-any-file-or-directory)

## Why did you do this

Yesterday, I had a talk with [Zach Zaro](http://zacharyzaro.com/), complaining
about the pain it is to reconfigure our Macbook each time we get a new one or
install from scratch. That's a talk we have already had months ago.

I change my workstation every X months. Each time I either lose my apps'
configurations, or I just waste a bunch of hours getting setup like I was on my
old box. I also spend a lot of time reconfiguring the same stuff again on all my
workstations (home, work).

Boring...

Some people tried to solve the problem on the application layer, like [Github's Boxen](https://boxen.github.com/),
but it solves a different problem, from my point of view. I don't spend a lot
of time installing or downloading stuff. I spend time configuring it.

For years, I've used a personal shell script that was copying known config
files into Subversion, Git or Dropbox, and linked them into my home. But I felt
a lot of us had the same problem: Making a more generic tool could help others
and I could get help from others to support more apps in the tool.

So here comes Mackup, the little tool that will sync all your application
configs to Dropbox (or Google Drive, or anything).

And it's [GPL](http://www.gnu.org/licenses/gpl.html), of course.

## What platforms are supported

- OS X
- GNU/Linux

## What's up with the weird name

Mackup is just a portmanteau of Mac and Backup. It is simple, short, and easy to
remember, and it corresponds with the whole idea of Mackup: the simpler – the better!
(And I suck at naming stuff, but who doesn't.)

## Where can I find more information

In the [doc](doc) directory.
