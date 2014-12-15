# Mackup

Keep your application settings in sync.

[![Circle CI](https://circleci.com/gh/lra/mackup.svg?style=shield)](https://circleci.com/gh/lra/mackup)
[![Coverage Status](https://img.shields.io/coveralls/lra/mackup.svg)](https://coveralls.io/r/lra/mackup?branch=master)
[![Code Health](https://landscape.io/github/lra/mackup/master/landscape.png)](https://landscape.io/github/lra/mackup/master)

## Quickstart

If you have Dropbox installed and want to use it to save your config files,
that's super easy.

On OS X, if you want an easy install, you can install
[Homebrew](http://brew.sh/) and do:
```bash
# Install Mackup
brew install mackup

# Launch it and back up your files
mackup backup
```

If not running OS X, or you don't like Homebrew, you can use PIP:
```bash
# Install Mackup with PIP
pip install mackup

# Launch it and back up your files
mackup backup
```

You're all set, and constantly backuped from now on.

Next, on any new workstation, do:
```bash
# Install Mackup
brew install mackup

# Launch it and restore your files
mackup restore
```

Done !

You can find more detailled instructions in [INSTALL.md](INSTALL.md)

## Usage

`mackup backup`

Backup your application settings.

`mackup restore`

Restore your application settings on a newly installed workstation.

`mackup uninstall`

Revert any synced config file to its original state, and delete the Mackup
folder in Dropbox. This will revert your system at pre-Mackup state.

`mackup list`

Display the list of applications supported by Mackup.

`mackup -h`

Get some help, obvious...

## What does it do ?

- Backups your application settings in a safe directory (e.g. Dropbox)
- Syncs your application settings among all your workstations
- Restores your configuration on any fresh install in one command line

By only tracking pure configuration files, it keeps the crap out of your
freshly new installed workstation (No cache, temporary and locally specific
files are transfered).

It also helps you spend more time doing real cool stuff, and less time setting
up your environment.

## Bullsh*t, what does it really do to my files ?!

Let's take `git` as an example. Your settings for `git` are saved in your home
folder, in the `.gitconfig` file.

### Backup

If you have Dropbox, when you launch `mackup backup`, here's what it's really
doing:

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

## Supported Storages

 - [Dropbox](https://www.dropbox.com/)
 - [Google Drive](https://drive.google.com/)
 - Anything able to sync a folder (e.g. [Git](http://git-scm.com/))

See the [README](doc/README.md) file in the doc directory for more info.

## Supported Applications

  - [1Password 4](https://agilebits.com/onepassword)
  - [Ack](http://beyondgrep.com/)
  - [Adium](http://adium.im/)
  - [Adobe Camera Raw](http://www.adobe.com/products/photoshop/extend.html)
  - [Adobe Lightroom](http://www.adobe.com/products/photoshop-lightroom.html)
  - [AppCode 2](http://www.jetbrains.com/objc/)
  - [aria2c](http://aria2.sourceforge.net/)
  - [Arara](http://cereda.github.io/arara/)
  - [Artistic Style](http://astyle.sourceforge.net)
  - [asciinema](https://asciinema.org/)
  - [Aspell](http://aspell.net/)
  - [Atom](https://atom.io/)
  - [AusKey](https://abr.gov.au/AUSkey/)
  - [Awareness](http://iamfutureproof.com/tools/awareness/)
  - [AWS Command Line Interface](https://aws.amazon.com/cli/)
  - [Bartender](http://www.macbartender.com/)
  - [Bash it](https://github.com/revans/bash-it/)
  - [Bash](http://www.gnu.org/software/bash/)
  - [BetterSnapTool](http://blog.boastr.net/)
  - [BetterTouchTool](http://blog.boastr.net/)
  - [BibDesk](http://bibdesk.sourceforge.net/)
  - [Billings Pro Server Admin](https://www.marketcircle.com/billingspro/download/billingspro-server/)
  - [Boto](https://github.com/boto/boto)
  - [Brackets](http://brackets.io/)
  - [Bundler](http://bundler.io)
  - [Byobu](http://byobu.co/)
  - [Caffeine](http://lightheadsw.com/caffeine/)
  - [Cartographica](http://www.macgis.com)
  - [Charles](http://www.charlesproxy.com)
  - [Chef](http://www.opscode.com/chef/)
  - [Chicken](http://sourceforge.net/projects/chicken/)
  - [Clementine](http://www.clementine-player.org/)
  - [ClipMenu](http://www.clipmenu.com/)
  - [CloudApp](http://getcloudapp.com/)
  - [Coda 2](http://panic.com/coda/)
  - [Colloquy](http://colloquy.info/)
  - [ColorSchemer Studio 2](http://www.colorschemer.com/osx_info.php)
  - [Composer](https://getcomposer.org/)
  - [Consular](http://www.rubydoc.info/github/achiu/consular/master/file/README.md)
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
  - [GHCi](http://www.haskell.org/haskellwiki/GHC/GHCi)
  - [Git Hooks](https://github.com/icefox/git-hooks)
  - [Git](http://git-scm.com/)
  - [Gitbox](http://gitboxapp.com/)
  - [Gmail Notifr](http://ashchan.com/projects/gmail-notifr)
  - [Go2Shell](http://zipzapmac.com/Go2Shell)
  - [GnuPG](http://www.gnupg.org/)
  - [GrandTotal 3](http://www.mediaatelier.com/GrandTotal3/)
  - [Hands Off!](http://www.oneperiodic.com/products/handsoff/)
  - [Hazel](http://www.noodlesoft.com/hazel.php)
  - [Heroku](https://www.heroku.com/)
  - [Hexels](http://hexraystudios.com/hexels/)
  - [Houdini](http://uglyapps.co.uk/houdini/)
  - [Htop](http://htop.sourceforge.net/)
  - [i2cssh](https://github.com/wouterdebie/i2cssh)
  - [IntelliJIDEA](http://www.jetbrains.com/idea/)
  - [Irssi](http://www.irssi.org/)
  - [iStat Menus 5](http://bjango.com/mac/istatmenus/)
  - [ITerm2](http://www.iterm2.com/)
  - [JSHint](http://www.jshint.com/)
  - [Janus](https://github.com/carlhuda/janus)
  - [jrnl](http://maebert.github.io/jrnl/)
  - [Julia](http://julialang.org)
  - [Kaleidoscope](http://www.kaleidoscopeapp.com/)
  - [Karabiner](https://pqrs.org/osx/karabiner)
  - [Keka](http://kekaosx.com/)
  - [Keybase](https://keybase.io/)
  - [Keymo](http://manytricks.com/keymo/)
  - [KeyRemap4MacBook](http://pqrs.org/macosx/keyremap4macbook/)
  - [LaTeXiT](http://www.chachatelier.fr/latexit/latexit-home.php?lang=en)
  - [LaunchBar](http://www.obdev.at/products/launchbar/index.html)
  - [Liftoff](http://github.com/thoughtbot/liftoff)
  - [Light Table](http://www.lighttable.com/)
  - [LimeChat](http://limechat.net/mac/)
  - [LittleSnitch](http://www.obdev.at/products/littlesnitch/)
  - [Livestreamer](http://livestreamer.tanuki.se/)
  - [MacOSX](http://www.apple.com/osx/)
  - [MacVim](https://code.google.com/p/macvim/)
  - [Magic Launch](https://www.oneperiodic.com/products/magiclaunch/)
  - [MagicPrefs](http://magicprefs.com/)
  - [Mailplane](http://mailplaneapp.com/)
  - [Max](http://sbooth.org/Max/)
  - [MenuMeters](http://www.ragingmenace.com/software/menumeters/)
  - [Mercurial](http://mercurial.selenic.com/)
  - [MercuryMover](http://www.heliumfoot.com/mercurymover/)
  - [Messages](http://www.apple.com/osx/apps/#messages)
  - [MySQL](http://www.mysql.com/)
  - [Moom](http://manytricks.com/moom/)
  - [Mou](http://mouapp.com/)
  - [mpd](http://www.musicpd.org)
  - [MPV](http://mpv.io/)
  - [Nano](http://www.nano-editor.org/)
  - [Navicat](http://navicat.com/)
  - [ncmpcpp](http://ncmpcpp.rybczak.net)
  - [newsbeuter](http://newsbeuter.org/)
  - [ngrok](https://ngrok.com/)
  - [nvALT](http://brettterpstra.com/projects/nvalt/)
  - [nvpy](https://github.com/cpbotha/nvpy)
  - [Oh My Fish](https://github.com/bpinto/oh-my-fish)
  - [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
  - [OmniFocus](http://www.omnigroup.com/products/omnifocus/)
  - [OmniGraffle](http://www.omnigroup.com/omnigraffle/)
  - [OpenSSH](http://www.openssh.org/)
  - [Pass](http://www.passwordstore.org/)
  - [Pastebot](http://tapbots.com/software/pastebot/)
  - [Path Finder](http://www.cocoatech.com/pathfinder/)
  - [Pear](http://pear.php.net/)
  - [Pentadactyl](http://5digits.org/pentadactyl/)
  - [Perl](http://www.perl.org/)
  - [Phoenix](https://github.com/sdegutis/Phoenix)
  - [PhpStorm](http://www.jetbrains.com/phpstorm/)
  - [PIP](http://www.pip-installer.org/)
  - [Poedit](http://poedit.net/)
  - [PokerStars](http://www.pokerstars.com/)
  - [PopClip](http://pilotmoon.com/popclip/)
  - [PostgreSQL](http://postgresql.org/)
  - [Pow](http://pow.cx/)
  - [Prezto](https://github.com/sorin-ionescu/prezto)
  - [Processing](http://processing.org/)
  - [Punto Switcher](http://punto.yandex.ru/)
  - [PyPI](https://pypi.python.org/pypi)
  - [Quicksilver](http://qsapp.com/)
  - [Rails](http://rubyonrails.org/)
  - [rTorrent](http://libtorrent.rakshasa.no/)
  - [R](http://www.r-project.org/)
  - [Rubocop](https://github.com/bbatsov/rubocop)
  - [Ruby Version](https://gist.github.com/fnichol/1912050)
  - [Ruby](http://ruby-lang.org/)
  - [RubyMine](http://www.jetbrains.com/ruby/)
  - [S3cmd](http://s3tools.org/s3cmd)
  - [SABnzbd](http://sabnzbd.org/)
  - [SBCL](http://www.sbcl.org/)
  - [SBT](http://www.scala-sbt.org/)
  - [Scenario](http://www.lagentesoft.com/scenario/)
  - [Screen](http://www.gnu.org/software/screen/)
  - [Screenhero](https://screenhero.com)
  - [Scrivener](http://www.literatureandlatte.com/scrivener.php)
  - [Scroll Reverser](https://pilotmoon.com/scrollreverser/)
  - [SelfControl](http://selfcontrolapp.com/)
  - [Seil](https://pqrs.org/macosx/keyremap4macbook/seil.html.en)
  - [Sequel Pro](http://www.sequelpro.com/)
  - [SHSH Blobs](http://en.wikipedia.org/wiki/SHSH_blob)
  - [Shuttle](http://fitztrev.github.io/shuttle/)
  - [SizeUp](http://www.irradiatedsoftware.com/sizeup/)
  - [Skim](http://skim-app.sourceforge.net/)
  - [Skitch](http://evernote.com/skitch/)
  - [Skype](http://www.skype.com/)
  - [Slate](https://github.com/jigish/slate)
  - [Slogger](http://brettterpstra.com/projects/slogger/)
  - [Soulver](http://www.acqualia.com/soulver/)
  - [SourceTree](http://sourcetreeapp.com)
  - [Spark](http://www.shadowlab.org/softwares/spark.php)
  - [Spectrwm](https://opensource.conformal.com/wiki/spectrwm)
  - [Spectacle](http://spectacleapp.com/)
  - [Spotify](https://www.spotify.com/)
  - [Stata](http://www.stata.com/)
  - [Stay](https://cordlessdog.com/stay/)
  - [Stickies](https://en.wikipedia.org/wiki/Stickies_%28software%29)
  - [Sublime Text](http://www.sublimetext.com/)
  - [Subversion](http://subversion.apache.org/)
  - [SuperDuper!](http://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html)
  - [TaskPaper](http://www.hogbaysoftware.com/products/taskpaper)
  - [Teamocil](http://remiprev.github.io/teamocil/)
  - [Terminator](https://launchpad.net/terminator/)
  - [TextMate](http://macromates.com/)
  - [Textual](http://www.codeux.com/textual/)
  - [Tig](https://github.com/jonas/tig)
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
  - [WebStorm 9](https://www.jetbrains.com/webstorm/)
  - [Wget](https://www.gnu.org/software/wget/)
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
configs to Dropbox (or Google Drive, or anything).

And it's [GPL](http://www.gnu.org/licenses/gpl.html) of course.

## What platform is supported ?

- OS X
- GNU/Linux

## What's up with the weird name ?

Mackup is just a contraction of Mac and Backup, I suck at naming stuff, ok.

## Where can I find more information ?

In the [doc](doc) directory.
