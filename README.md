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
curl -o mackup https://raw.github.com/lra/mackup/master/mackup.py

# Make it executable
chmod +x mackup

# Launch it and restore your files from Dropbox
./mackup restore
```

Done !

## Install

```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/master/mackup.py

# Make it executable
chmod +x mackup

# Copy it to your path
sudo mv mackup /usr/bin/mackup

# Launch it
mackup backup
```

## Upgrade

Same as Install:

```bash
# Download Mackup
curl -o mackup https://raw.github.com/lra/mackup/master/mackup.py

# Make it executable
chmod +x mackup

# Copy it to your path
sudo mv mackup /usr/bin/mackup

# Launch it
mackup backup
```

It will add support for any application you were missing before.

## Uninstall

You can revert all your files to their original state.
```bash
# Just run this
mackup uninstall
```
This will move back any file from Dropbox to its original place in your home
folder and destroy the Mackup folder in Dropbox.

## Usage

`mackup backup`

Backup your application settings in Dropbox.

`mackup restore`

Restore your application settings on a newly installed workstation.

`mackup uninstall`

Revert any synced config file to its original state, and delete the Mackup
folder in Dropbox. This will revert your system at pre-Mackup state.

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

  - [Adium](http://adium.im/)
  - [Adobe Lightroom](http://www.adobe.com/products/photoshop-lightroom.html)
  - [AppCode 2](http://www.jetbrains.com/objc/)
  - [Bartender](http://www.macbartender.com/)
  - [Bash](http://www.gnu.org/software/bash/)
  - [BetterSnapTool](http://blog.boastr.net/)
  - [BetterTouchTool](http://blog.boastr.net/)
  - [BibDesk](http://bibdesk.sourceforge.net/)
  - [Boto](https://github.com/boto/boto)
  - [Byobu](http://byobu.co/)
  - [Caffeine](http://lightheadsw.com/caffeine/)
  - [Chef](http://www.opscode.com/chef/)
  - [ClipMenu](http://www.clipmenu.com/)
  - [CloudApp](http://getcloudapp.com/)
  - [Coda 2](http://panic.com/coda/)
  - [Concentrate](http://www.getconcentrating.com/)
  - [ControlPlane](http://www.controlplaneapp.com/)
  - [CoRD](http://cord.sourceforge.net/)
  - [Droplr](https://droplr.com/hello)
  - [Emacs](http://www.gnu.org/software/emacs/)
  - [ExpanDrive](http://www.expandrive.com/)
  - [Fantastical](http://flexibits.com/fantastical)
  - [Fish](http://ridiculousfish.com/shell/)
  - [Flux](http://stereopsis.com/flux/)
  - [GeekTool](http://projects.tynsoe.org/en/geektool/)
  - [Git](http://git-scm.com/)
  - [Git Hooks](https://github.com/icefox/git-hooks)
  - [Gitbox](http://gitboxapp.com/)
  - [GnuPG](http://www.gnupg.org/)
  - [Heroku](https://www.heroku.com/)
  - [Htop](http://htop.sourceforge.net/)
  - [IntelliJIDEA 12](http://www.jetbrains.com/idea/)
  - [Irssi](http://www.irssi.org/)
  - [ITerm2](http://www.iterm2.com/)
  - [Janus](https://github.com/carlhuda/janus)
  - [Keymo](http://manytricks.com/keymo/)
  - [KeyRemap4MacBook](http://pqrs.org/macosx/keyremap4macbook/)
  - [LimeChat](http://limechat.net/mac/)
  - [MacOSX](http://www.apple.com/osx/)
  - [MacVim](https://code.google.com/p/macvim/)
  - [Mailplane](http://mailplaneapp.com/)
  - [MenuMeters](http://www.ragingmenace.com/software/menumeters/)
  - [Mercurial](http://mercurial.selenic.com/)
  - [MercuryMover](http://www.heliumfoot.com/mercurymover/)
  - [Moom](http://manytricks.com/moom/)
  - [MPV](http://mpv.io/)
  - [Nano](http://www.nano-editor.org/)
  - [nvALT](http://brettterpstra.com/projects/nvalt/)
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [OmniFocus](http://www.omnigroup.com/products/omnifocus/)
  - [OpenSSH](http://www.openssh.org/)
  - [Pastebot](http://tapbots.com/software/pastebot/)
  - [PCKeyboardHack](http://pqrs.org/macosx/keyremap4macbook/pckeyboardhack.html.en)
  - [Pear](http://pear.php.net/)
  - [Pentadactyl](http://5digits.org/pentadactyl/)
  - [PhpStorm 6](http://www.jetbrains.com/phpstorm/)
  - [PIP](http://www.pip-installer.org/)
  - [PopClip](http://pilotmoon.com/popclip/)
  - [Pow](http://pow.cx/)
  - [PyPI](https://pypi.python.org/pypi)
  - [Quicksilver](http://qsapp.com/)
  - [Rails](http://rubyonrails.org/)
  - [Ruby Version](https://gist.github.com/fnichol/1912050)
  - [Ruby](http://ruby-lang.org/)
  - [RubyMine 4](http://www.jetbrains.com/ruby/)
  - [RubyMine 5](http://www.jetbrains.com/ruby/)
  - [S3cmd](http://s3tools.org/s3cmd)
  - [Screen](http://www.gnu.org/software/screen/)
  - [Sequel Pro](http://www.sequelpro.com/)
  - [SHSH Blobs](http://en.wikipedia.org/wiki/SHSH_blob)
  - [SizeUp](http://www.irradiatedsoftware.com/sizeup/)
  - [Slate](https://github.com/jigish/slate)
  - [Slogger](http://brettterpstra.com/projects/slogger/)
  - [SourceTree](http://sourcetreeapp.com)
  - [Spark](http://www.shadowlab.org/softwares/spark.php)
  - [Spotify](https://www.spotify.com/)
  - [Sublime Text](http://www.sublimetext.com/)
  - [Subversion](http://subversion.apache.org/)
  - [Teamocil](http://remiprev.github.io/teamocil/)
  - [TextMate](http://macromates.com/)
  - [Tmux](http://tmux.sourceforge.net/)
  - [Tmuxinator](https://github.com/aziz/tmuxinator)
  - [Transmission](http://www.transmissionbt.com/)
  - [Transmit](http://panic.com/transmit/)
  - [uTorrent](http://www.utorrent.com/)
  - [Ventrilo](http://www.ventrilo.com/)
  - [Vim](http://www.vim.org/)
  - [Vimperator](http://www.vimperator.org/vimperator)
  - [Viscosity](http://www.sparklabs.com/viscosity/)
  - [Witch](http://manytricks.com/witch/)
  - [X11](http://www.x.org/)
  - [XCode](https://developer.apple.com/xcode/)
  - [XEmacs](http://www.xemacs.org/)
  - [Zsh](http://zsh.sourceforge.net/)

You can add your favorite application by forking it and doing a
[Pull Request](https://help.github.com/articles/using-pull-requests).

## I don't understand, how can I get support for my beloved app ?

Open a [new issue](https://github.com/lra/mackup/issues).

## How can I tell Mackup to not sync an application ?

In your home folder, create a file named `.mackup.cfg` and add the application
names to ignore in the `Ignored Applications` section, one by line.

```ini
# Example, to not sync SSH and Adium:
[Ignored Applications]
SSH
Adium
```

A [sample](.mackup.cfg) of this file is available for download:

```bash
cd
curl -o .mackup.cfg https://raw.github.com/lra/mackup/master/.mackup.cfg
```
Be careful, if you download it like this, Mackup will ignore SSH and Adium from
now on !

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
