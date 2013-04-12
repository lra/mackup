# Mackup

Keep your Mac application settings in sync.

## Quickstart

Install [Dropbox](http://www.dropbox.com/) first, it's needed.

On your current Mac:
```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/master/mackup.py

# Make it executable
chmod +x mackup

# Launch it and back up your files in Dropbox
./mackup backup
```

You're all set, and constantly backuped from now on.

Next, on any new Mac, install Dropbox and do:
```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/0.1/mackup.py

# Make it executable
chmod +x mackup

# Launch it and restore your files from Dropbox
./mackup restore
```

Done !

## Install

```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/0.1/mackup.py

# Make it executable
chmod +x mackup

# Copy it to your path
sudo mv mackup /usr/bin/mackup

# Launch it
mackup backup
```

## Uninstall

```bash
# Just delete it
sudo rm /usr/bin/mackup
```

## Usage

`mackup backup`

Backup your application settings in Dropbox.

`mackup restore`

Restore your application settings on a newly installed workstation.

`mackup -h`

Get some help, obvious...

## What does it do ?

- Backups your application settings in Dropbox
- Syncs your application settings among all your workstations
- Restores your configuration on any fresh install in one command line

By only tracking pure configuration files, it keeps the crap out of your freshly
new installed workstation (No cache, temporary and locally specific files are
transfered).

It also helps you spend more time doing real cool stuff, and less time setting
you environment.

## Bullsh*t, what does it really do to my files ?!

Let's take `git` as an example. Your settings for `git` are saved in your home
folder, in the `.gitconfig` file.

### Backup

When you launch `mackup backup`, here's what it's really doing:

1. `cp ~/.gitconfig ~/Dropbox/Mackup/.gitconfig`
1. `rm ~/.gitconfig`
1. `ln -s ~/Dropbox/Mackup/.gitconfig ~/.gitconfig`

Now your `git` config is always backup and up to date on all your Macs.

### Restore

When you launch `mackup restore`, here's what it's really doing:

1. `ln -s ~/Dropbox/Mackup/.gitconfig ~/.gitconfig`

That's it, you got your `git` config setup on your new Mac.

`mackup` does the same for any supported application.

## Supported Applications

  - [Bash](http://www.gnu.org/software/bash/)
  - [Boto](https://github.com/boto/boto)
  - [Emacs](http://www.gnu.org/software/emacs/)
  - [Git](http://git-scm.com/)
  - [GnuPG](http://www.gnupg.org/)
  - [LimeChat](http://limechat.net/mac/)
  - [MacOSX](http://www.apple.com/osx/)
  - [Mercurial](http://mercurial.selenic.com/)
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [OpenSSH](http://www.openssh.org/)
  - [Pow](http://pow.cx/)
  - [Rails](http://rubyonrails.org/)
  - [Ruby](http://ruby-lang.org/)
  - [S3cmd](http://s3tools.org/s3cmd)
  - [Sequel Pro](http://www.sequelpro.com/)
  - [Sublime Text 2](http://www.sublimetext.com/)
  - [Subversion](http://subversion.apache.org/)
  - [Vim](http://www.vim.org/)
  - [X11](http://www.x.org/)
  - [XEmacs](http://www.xemacs.org/)
  - [Zsh](http://zsh.sourceforge.net/)

You can add your favorite application by forking it and doing a
[Pull Request](https://help.github.com/articles/using-pull-requests).

## I don't understand, how can I get support for my beloved app ?

Open a [new issue](https://github.com/lra/mackup/issues).

## Why did you do this ?!

Yesterday, I had a talk with [Zach Zaro](http://zacharyzaro.com/), complaining
about the pain it is to reconfigure our Macbook each time we get a new one or
install from scratch. That's a talk we already had months ago.

I change my workstation every X months. Each time I either loose the
configuration of all the apps I use, or I just waste a bunch of hours getting
setup like I was on my old box. I also spent a lot of time reconfiguring the
same stuff again on all my workstations (home, work)

Boring...

Some people tried to solve the problem on the application layer, like
[Github's Boxen](http://boxen.github.com/), but I feel like it solves a non
problem: I don't really spend time installing stuff, mostly downloading: I
spend time configuring it.

For years, I've used a personnal shell script that was copying known config
files into Subversion, Git or Dropbox, and linked them into my home. But I felt
a lot of us had the same problem: Making a more generic tool could help others
and I could get help from others to support more apps in the tool.

So here comes Mackup, the little tool that will sync all your application
configs to Dropbox.

And it's [GPL](http://www.gnu.org/licenses/gpl.html) of course.

## What platform is supported ?

- OS X

## What's up with the weird name ?

Mackup is just a contraction of Mac and Backup, I suck at naming stuff, ok.
