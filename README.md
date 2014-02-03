# Mackup

Keep your application settings in sync.

[![Build Status](https://travis-ci.org/lra/mackup.png?branch=master)](https://travis-ci.org/lra/mackup)
[![Coverage Status](https://coveralls.io/repos/lra/mackup/badge.png)](https://coveralls.io/r/lra/mackup)
[![Code Health](https://landscape.io/github/lra/mackup/master/landscape.png)](https://landscape.io/github/lra/mackup/master)

## Quickstart

Install [Dropbox](http://www.dropbox.com/) first, it's needed.

On OS X, if you want an easy install, you can install [Homebrew](http://brew.sh/) and do:
```bash
# Install Mackup
brew install mackup

# Launch it and back up your files in Dropbox
mackup backup
```

If not running OS X, or you don't like Homebrew, run on your current workstation:
```bash
# Download Mackup
curl -o mackup.zip https://codeload.github.com/lra/mackup/zip/master

# Uncompress the archive
unzip mackup.zip

# Launch it and back up your files in Dropbox
./mackup-master/bin/mackup backup
```

You're all set, and constantly backuped from now on.

Next, on any new workstation, install Dropbox and do:
```bash
# Install Mackup
brew install mackup

# Launch it and restore your files from Dropbox
mackup restore
```

Done !

You can find more detailled instructions in [INSTALL.md](INSTALL.md)

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

Now your `git` config is always backup and up to date on all your workstations.

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
This will move back any file from Dropbox to its original place in your home
folder and destroy the Mackup folder in Dropbox.

## Supported Applications

  - [Ack](http://beyondgrep.com/)
  - [Adium](http://adium.im/)
  - [Adobe Camera Raw](http://www.adobe.com/products/photoshop/extend.html)
  - [Adobe Lightroom](http://www.adobe.com/products/photoshop-lightroom.html)
  - [AppCode 2](http://www.jetbrains.com/objc/)
  - [Arara](http://cereda.github.io/arara/)
  - [Aspell](http://aspell.net/)
  - [Awareness](http://iamfutureproof.com/tools/awareness/)
  - [Bartender](http://www.macbartender.com/)
  - [Bash it](https://github.com/revans/bash-it/)
  - [Bash](http://www.gnu.org/software/bash/)
  - [BetterSnapTool](http://blog.boastr.net/)
  - [BetterTouchTool](http://blog.boastr.net/)
  - [BibDesk](http://bibdesk.sourceforge.net/)
  - [Boto](https://github.com/boto/boto)
  - [Bundler](http://bundler.io)
  - [Byobu](http://byobu.co/)
  - [Caffeine](http://lightheadsw.com/caffeine/)
  - [Chef](http://www.opscode.com/chef/)
  - [Chicken](http://sourceforge.net/projects/chicken/)
  - [Clementine](http://www.clementine-player.org/)
  - [ClipMenu](http://www.clipmenu.com/)
  - [CloudApp](http://getcloudapp.com/)
  - [Coda 2](http://panic.com/coda/)
  - [Colloquy](http://colloquy.info/)
  - [Concentrate](http://www.getconcentrating.com/)
  - [ControlPlane](http://www.controlplaneapp.com/)
  - [CoRD](http://cord.sourceforge.net/)
  - [Cyberduck](http://cyberduck.ch/)
  - [Dash](http://kapeli.com/dash)
  - [Deal Alert](http://dealalertapp.com/)
  - [Default Folder X](http://www.stclairsoft.com/DefaultFolderX/)
  - [Divvy](http://mizage.com/divvy/)
  - [Dolphin](https://dolphin-emu.org/)
  - [Droplr](https://droplr.com/hello)
  - [Emacs](http://www.gnu.org/software/emacs/)
  - [Enjoyable](http://yukkurigames.com/enjoyable/)
  - [Exercism](http://exercism.io/)
  - [ExpanDrive](http://www.expandrive.com/)
  - [Fantastical](http://flexibits.com/fantastical)
  - [Feeds](http://www.feedsapp.com/)
  - [Filezilla](https://filezilla-project.org/)
  - [Fish](http://ridiculousfish.com/shell/)
  - [Flux](http://stereopsis.com/flux/)
  - [FontExplorer X](http://www.fontexplorerx.com/)
  - [ForkLift 2](http://www.binarynights.com/forklift/)
  - [GeekTool](http://projects.tynsoe.org/en/geektool/)
  - [Git Hooks](https://github.com/icefox/git-hooks)
  - [Git](http://git-scm.com/)
  - [Gitbox](http://gitboxapp.com/)
  - [Gmail Notifr](http://ashchan.com/projects/gmail-notifr)
  - [GnuPG](http://www.gnupg.org/)
  - [Hands Off!](http://www.oneperiodic.com/products/handsoff/)
  - [Heroku](https://www.heroku.com/)
  - [Hexels](http://hexraystudios.com/hexels/)
  - [Htop](http://htop.sourceforge.net/)
  - [i2cssh](https://github.com/wouterdebie/i2cssh)
  - [IntelliJIDEA 12](http://www.jetbrains.com/idea/)
  - [Irssi](http://www.irssi.org/)
  - [ITerm2](http://www.iterm2.com/)
  - [Janus](https://github.com/carlhuda/janus)
  - [Keka](http://kekaosx.com/)
  - [Keymo](http://manytricks.com/keymo/)
  - [KeyRemap4MacBook](http://pqrs.org/macosx/keyremap4macbook/)
  - [LaTeXiT](http://www.chachatelier.fr/latexit/latexit-home.php?lang=en)
  - [LaunchBar](http://www.obdev.at/products/launchbar/index.html)
  - [Light Table](http://www.lighttable.com/)
  - [LimeChat](http://limechat.net/mac/)
  - [LittleSnitch](http://www.obdev.at/products/littlesnitch/)
  - [Livestreamer](http://livestreamer.tanuki.se/)
  - [MacOSX](http://www.apple.com/osx/)
  - [MacVim](https://code.google.com/p/macvim/)
  - [MagicPrefs](http://magicprefs.com/)
  - [Mailplane](http://mailplaneapp.com/)
  - [MenuMeters](http://www.ragingmenace.com/software/menumeters/)
  - [Mercurial](http://mercurial.selenic.com/)
  - [MercuryMover](http://www.heliumfoot.com/mercurymover/)
  - [Messages](http://www.apple.com/osx/apps/#messages)
  - [Moom](http://manytricks.com/moom/)
  - [Mou](http://mouapp.com/)
  - [mpd](http://www.musicpd.org)
  - [MPV](http://mpv.io/)
  - [Nano](http://www.nano-editor.org/)
  - [ncmpcpp](http://ncmpcpp.rybczak.net)
  - [nvALT](http://brettterpstra.com/projects/nvalt/)
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [OmniFocus](http://www.omnigroup.com/products/omnifocus/)
  - [OmniGraffle](http://www.omnigroup.com/omnigraffle/)
  - [OpenSSH](http://www.openssh.org/)
  - [Pastebot](http://tapbots.com/software/pastebot/)
  - [Path Finder](http://www.cocoatech.com/pathfinder/)
  - [PCKeyboardHack](http://pqrs.org/macosx/keyremap4macbook/pckeyboardhack.html.en)
  - [Pear](http://pear.php.net/)
  - [Pentadactyl](http://5digits.org/pentadactyl/)
  - [PhpStorm 6](http://www.jetbrains.com/phpstorm/)
  - [PIP](http://www.pip-installer.org/)
  - [PokerStars](http://www.pokerstars.com/)
  - [PopClip](http://pilotmoon.com/popclip/)
  - [Pow](http://pow.cx/)
  - [PyPI](https://pypi.python.org/pypi)
  - [Quicksilver](http://qsapp.com/)
  - [Rails](http://rubyonrails.org/)
  - [rTorrent](http://libtorrent.rakshasa.no/)
  - [Ruby Version](https://gist.github.com/fnichol/1912050)
  - [Ruby](http://ruby-lang.org/)
  - [RubyMine 4](http://www.jetbrains.com/ruby/)
  - [RubyMine 5](http://www.jetbrains.com/ruby/)
  - [S3cmd](http://s3tools.org/s3cmd)
  - [SABnzbd](http://sabnzbd.org/)
  - [Scenario](http://www.lagentesoft.com/scenario/)
  - [Screen](http://www.gnu.org/software/screen/)
  - [SelfControl](http://selfcontrolapp.com/)
  - [Sequel Pro](http://www.sequelpro.com/)
  - [SHSH Blobs](http://en.wikipedia.org/wiki/SHSH_blob)
  - [Shuttle](http://fitztrev.github.io/shuttle/)
  - [SizeUp](http://www.irradiatedsoftware.com/sizeup/)
  - [Skim](http://skim-app.sourceforge.net/)
  - [Skitch](http://evernote.com/skitch/)
  - [Skype](http://www.skype.com/)
  - [Slate](https://github.com/jigish/slate)
  - [Slogger](http://brettterpstra.com/projects/slogger/)
  - [SourceTree](http://sourcetreeapp.com)
  - [Spark](http://www.shadowlab.org/softwares/spark.php)
  - [Spectacle](http://spectacleapp.com/)
  - [Spotify](https://www.spotify.com/)
  - [Stata](http://www.stata.com/)
  - [Sublime Text](http://www.sublimetext.com/)
  - [Subversion](http://subversion.apache.org/)
  - [SuperDuper!](http://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html)
  - [Teamocil](http://remiprev.github.io/teamocil/)
  - [TextMate](http://macromates.com/)
  - [Textual](http://www.codeux.com/textual/)
  - [Tmux](http://tmux.sourceforge.net/)
  - [Tmuxinator](https://github.com/aziz/tmuxinator)
  - [Tower](http://www.git-tower.com/)
  - [Transmission](http://www.transmissionbt.com/)
  - [Transmit](http://panic.com/transmit/)
  - [Twitterrific](http://twitterrific.com/)
  - [uTorrent](http://www.utorrent.com/)
  - [Ventrilo](http://www.ventrilo.com/)
  - [Vim](http://www.vim.org/)
  - [Vimperator](http://www.vimperator.org/vimperator)
  - [Viscosity](http://www.sparklabs.com/viscosity/)
  - [Witch](http://manytricks.com/witch/)
  - [X11](http://www.x.org/)
  - [Xchat](http://www.xchat.org/)
  - [XCode](https://developer.apple.com/xcode/)
  - [XEmacs](http://www.xemacs.org/)
  - [XLD](http://tmkk.undo.jp/xld/)
  - [Zsh](http://zsh.sourceforge.net/)
  - iTunes Applescripts

You can add your favorite application by forking it and doing a
[Pull Request](https://help.github.com/articles/using-pull-requests).

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
- GNU/Linux

## What's up with the weird name ?

Mackup is just a contraction of Mac and Backup, I suck at naming stuff, ok.

## Where can I find more information ?

In the [doc](doc) directory.
