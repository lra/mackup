# Mackup

Keep you application settings in sync

## Quickstart

Install [Dropbox](http://www.dropbox.com/) first, it's needed.

Then:
```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/master/mackup

# Make it executable
chmod +x mackup

# Launch it and back up your files in Dropbox
./mackup backup
```

## Usage

`mackup backup`

Backup your application settings in Dropbox.

`mackup restore`

Restore your application settings on a newly installed workstation.

## What does it do ?

- Backup your application settings in Dropbox
- Sync your application settings among all your workstations
- Restore your configuration on any fresh install in one command line

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

  - Bash
  - Git
  - Mercurial
  - S3cmd
  - X11

You can add your favorite application by forking it and doing a
[Pull Request](https://help.github.com/articles/using-pull-requests)

## I don't understand, how can I get support for my beloved app ?

Open a [new issue](https://github.com/lra/mackup/issues)

## Why did you do this ?!

Nowadays, I change my workstation every X months. Each time I either loose the
configuration of all the apps I use, or I just waste a bunch of hours getting
setup like I was on my old box.

Some people tried to solve the problem on the application layer, like [Github's
Boxen](http://boxen.github.com/), but I feel like it solves a non problem: I
don't really spend time installing stuff, I spend time configuring it.

For years, I've used a personnal shell script that was copying known config
files into `svn`, `git` or Dropbox, and linked them into my home. But, like
the [Homebrew](http://mxcl.github.io/homebrew/) guys, I felt a lot of us had the
same problem, and I could get help from others to support more apps.

So here it is.

## What platform is supported ?

1. OS X

## What's up with the weird name ?

Mackup is just a contraction of Mac and Backup, I suck at naming stuff, ok.
