# Mackup

Keep your application settings in sync.

[![Circle CI](https://circleci.com/gh/lra/mackup.svg?style=shield)](https://circleci.com/gh/lra/mackup)
[![codecov.io](https://codecov.io/github/lra/mackup/coverage.svg?branch=master)](http://codecov.io/github/lra/mackup?branch=master)

## Table of content

- [Quickstart](#quickstart)
- [Usage](#usage)
- [What does it do](#what-does-it-do)
- [Bullsh*t, what does it really do to my files](#bullsht-what-does-it-really-do-to-my-files)
- [Supported Storages](#supported-storages)
- [Supported Applications](#supported-applications)
- [Can you support application X](#can-you-support-application-x)
- [Why did you do this](#why-did-you-do-this)
- [What platforms are supported](#what-platforms-are-supported)
- [What's up with the weird name](#what-s-up-with-the-weird-name)
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

## Bullsh*t, what does it really do to my files

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

- [1Password 4](https://agilebits.com/onepassword)
- [Ack](http://beyondgrep.com/)
- [Adium](https://adium.im/)
- [Adobe Camera Raw](http://www.adobe.com/products/photoshop/extend.html)
- [Adobe Illustrator CC](https://www.adobe.com/products/illustrator.html)
- [Adobe Photoshop CC](http://www.adobe.com/products/photoshop.html)
- [Adobe Photoshop Lightroom CC](https://www.adobe.com/products/photoshop-lightroom.html)
- [Airmail](http://airmailapp.com/)
- [Amethyst](https://ianyh.com/amethyst/)
- [Amphetamine](https://itunes.apple.com/us/app/amphetamine/id937984704)
- [Ancient Domains of Mystery](http://www.adom.de/home/index.html)
- [Android Studio](https://developer.android.com/sdk/)
- [Ansible](http://www.ansible.com/)
- [AppCleaner](http://freemacsoft.net/appcleaner/)
- [AppCode](http://www.jetbrains.com/objc/)
- [Apptivate](http://www.apptivateapp.com/)
- [Arara](https://github.com/cereda/arara)
- [aria2c](http://aria2.sourceforge.net/)
- [Arm](https://www.atagar.com/arm/)
- [Artistic Style](http://astyle.sourceforge.net)
- [asciinema](https://asciinema.org/)
- [Aspell](http://aspell.net/)
- [Atlantis](http://www.riverdark.net/atlantis/)
- [Atom](https://atom.io/)
- [Audacious](http://audacious-media-player.org/)
- [AusKey](https://abr.gov.au/AUSkey/)
- [Autokey](https://code.google.com/p/autokey/)
- [Awareness](http://iamfutureproof.com/tools/awareness/)
- [AWS Command Line Interface](https://aws.amazon.com/cli/)
- [Bartender](http://www.macbartender.com/)
- [Bash it](https://github.com/Bash-it/bash-it)
- [Bash](http://www.gnu.org/software/bash/)
- [BBEdit](http://www.barebones.com/products/bbedit/)
- [Beatport Pro](https://www.beatport.com/desktop)
- [BetterSnapTool](http://www.boastr.net/)
- [BetterTouchTool](http://www.boastr.net/)
- [BibDesk](http://bibdesk.sourceforge.net/)
- [Billings Pro Server Admin](https://www.marketcircle.com/billingspro/download/billingspro-server/)
- [Bitchx](http://www.bitchx.org/)
- [Blackfire](https://blackfire.io/)
- [Blender](https://blender.org/)
- [Boto](https://github.com/boto/boto)
- [Boxer](http://boxerapp.com)
- [Brackets](http://brackets.io/)
- [Bundler](http://bundler.io)
- [Byobu](http://byobu.co/)
- [Caffeine](http://lightheadsw.com/caffeine/)
- [Capture One](http://www.phaseone.com/Imaging-Software/Capture-One.aspx)
- [Cartographica](https://www.macgis.com/)
- [Cerebro](https://cerebroapp.com/)
- [Charles](http://www.charlesproxy.com)
- [Chef](https://www.chef.io/chef/)
- [Chicken](http://sourceforge.net/projects/chicken/)
- [Clementine](https://www.clementine-player.org/)
- [CLion](https://www.jetbrains.com/clion/)
- [ClipMenu](http://www.clipmenu.com/)
- [Clipy](https://clipy-app.com/)
- [CloudApp](http://getcloudapp.com/)
- [Coda 2](http://panic.com/coda/)
- [Colloquy](http://colloquy.info/)
- [ColorSchemer Studio 2](http://www.colorschemer.com/osx_info.php)
- [ColorSync](https://en.wikipedia.org/wiki/ColorSync)
- [Composer](https://getcomposer.org/)
- [Concentrate](http://www.getconcentrating.com/)
- [Conky](https://github.com/brndnmtthws/conky)
- [Consular](https://github.com/achiu/consular)
- [ControlPlane](http://www.controlplaneapp.com/)
- [CopyQ](https://github.com/hluk/CopyQ)
- [CoRD](http://cord.sourceforge.net/)
- [CotEditor](http://coteditor.com/)
- [Ctags](http://ctags.sourceforge.net/)
- [Cyberduck](https://cyberduck.io/)
- [DaisyDisk](https://daisydiskapp.com)
- [Dash](https://kapeli.com/dash)
- [Day-O](http://www.shauninman.com/archive/2011/10/20/day_o_mac_menu_bar_clock)
- [DbVisualizer](https://www.dbvis.com/)
- [Deal Alert](http://dealalertapp.com/)
- [Default Folder X](http://www.stclairsoft.com/DefaultFolderX/)
- [Devil's Pie 2](http://www.gusnan.se/devilspie2/)
- [Devil's Pie](https://en.wikipedia.org/wiki/Devil's_Pie_(software))
- [dig](http://en.wikipedia.org/wiki/Dig_(command))
- [Divvy](http://mizage.com/divvy/)
- [Docker](https://www.docker.com/)
- [Dolphin](https://dolphin-emu.org/)
- [Double Commander](http://doublecmd.sourceforge.net/)
- [Doxie](http://www.getdoxie.com/)
- [Droplr](https://droplr.com/)
- [Dropzone 3](https://aptonic.com/dropzone3/)
- [Drush](http://www.drush.org/)
- [EditorConfig](http://editorconfig.org/)
- [Electrum](https://electrum.org/#home)
- [Emacs](http://www.gnu.org/software/emacs/)
- [Enjoyable](https://yukkurigames.com/enjoyable/)
- [Environmental Station Alpha](http://www.hempuli.com/esa/)
- [Exercism](http://exercism.io/)
- [ExpanDrive](http://www.expandrive.com/)
- [Factorio](https://www.factorio.com)
- [Fantastical](http://flexibits.com/fantastical)
- [fasd](https://github.com/clvv/fasd)
- [fastlane](https://fastlane.tools)
- [Feeds](http://www.feedsapp.com/)
- [FileZilla](https://filezilla-project.org/)
- [Fish](http://ridiculousfish.com/shell/)
- [Fisherman](http://fisherman.sh/)
- [FlexGet](http://flexget.com/)
- [Flux](https://justgetflux.com/)
- [Fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/)
- [FontExplorer X](http://www.fontexplorerx.com/)
- [Forge](http://www.slightlymagic.net/wiki/Forge)
- [ForkLift 2](http://www.binarynights.com/forklift/)
- [Franz](https://meetfranz.com)
- [Gas Mask](https://github.com/2ndalpha/gasmask/)
- [gdb](https://www.gnu.org/software/gdb/)
- [Gear Player](https://www.gearmusicplayer.com/)
- [GeekTool](http://projects.tynsoe.org/en/geektool/)
- [GHCi](https://wiki.haskell.org/GHC/GHCi)
- [Ghostwriter](https://wereturtle.github.io/ghostwriter/)
- [Git Hooks](https://github.com/icefox/git-hooks)
- [Git](http://git-scm.com/)
- [Gitbox](http://gitboxapp.com/)
- [GitKraken](https://www.gitkraken.com)
- [GitUp](http://gitup.co/)
- [Gmail Notifr](http://ashchan.com/projects/gmail-notifr)
- [GMVault](http://gmvault.org/)
- [Gnome SSH Tunnel Manager](http://sourceforge.net/projects/gstm/)
- [GnuPG](https://www.gnupg.org/)  (NOTE: includes private keys)
- [Go2Shell](http://zipzapmac.com/Go2Shell)
- [Gogland](https://www.jetbrains.com/go/)
- [GoShare](https://github.com/dictget/goshare)
- [Gradle](http://gradle.org)
- [GrandTotal 3](http://www.mediaatelier.com/GrandTotal4/)
- [Hammerspoon](http://www.hammerspoon.org/)
- [HandBrake](https://handbrake.fr/)
- [Hands Off!](http://www.oneperiodic.com/products/handsoff/)
- [Hazel](http://www.noodlesoft.com/hazel.php)
- [Hero Lab](http://www.wolflair.com/index.php?context=hero_lab)
- [Heroku](https://www.heroku.com/)
- [HexChat](https://hexchat.github.io/)
- [Hexels](http://hexraystudios.com/hexels/)
- [Homebridge](https://github.com/nfarina/homebridge)
- [Houdini](http://uglyapps.co.uk/houdini/)
- [Htop](http://htop.sourceforge.net/)
- [HTTPie](https://httpie.org/)
- [Hyper.app](https://hyper.is/)
- [HyperDock](https://bahoom.com/hyperdock)
- [HyperSwitch](https://bahoom.com/hyperswitch)
- [i2cssh](https://github.com/wouterdebie/i2cssh)
- [i3](https://i3wm.org/)
- [i3wm](http://i3wm.org/)
- [IdeaVim](https://github.com/JetBrains/ideavim)
- [Insomnia](https://insomnia.rest/)
- [IntelliJIDEA](http://www.jetbrains.com/idea/)
- [IPython](http://ipython.org/)
- [Irssi](http://www.irssi.org/)
- [iStat Menus 5](https://bjango.com/mac/istatmenus/)
- [iTerm2](https://www.iterm2.com/)
- [iTermocil](https://github.com/TomAnthony/itermocil)
- [Janus](https://github.com/carlhuda/janus)
- [Jitouch](http://www.jitouch.com/)
- [jrnl](http://maebert.github.io/jrnl/)
- [JSHint](http://jshint.com/)
- [Julia](http://julialang.org)
- [Jumpcut](http://jumpcut.sourceforge.net/)
- [Jupyter](http://jupyter.org/)
- [Kaleidoscope](http://www.kaleidoscopeapp.com/)
- [Karabiner Elements](https://github.com/tekezo/Karabiner-Elements)
- [Karabiner](https://pqrs.org/osx/karabiner/)
- [Kdenlive](https://kdenlive.org/)
- [KeePassX](http://www.keepassx.org/)
- [KeepingYouAwake](https://github.com/newmarcel/KeepingYouAwake)
- [Keka](http://www.kekaosx.com/en/)
- [Keybase](https://keybase.io/)
- [Keyboard Maestro](http://www.keyboardmaestro.com)
- [Keymo](http://manytricks.com/keymo/)
- [KeyRemap4MacBook](https://pqrs.org/osx/karabiner/)
- [Kwm](https://koekeishiya.github.io/kwm/)
- [LaTeXiT](http://www.chachatelier.fr/latexit/latexit-home.php?lang=en)
- [LaunchBar](https://www.obdev.at/products/launchbar/index.html)
- [LibreOffice](https://www.libreoffice.org/)
- [Liftoff](https://github.com/thoughtbot/liftoff)
- [Light Table](http://lighttable.com/)
- [LimeChat](http://limechat.net/mac/)
- [Liquid Prompt](https://github.com/nojhan/liquidprompt)
- [LittleSnitch](http://www.obdev.at/products/littlesnitch/)
- [Livestreamer](http://livestreamer.tanuki.se/)
- [Lollypop](https://gnumdk.github.io/lollypop-web/)
- [Luftrausers](http://luftrausers.com)
- [MacDive](http://www.mac-dive.com/)
- [MacDown](http://macdown.uranusjr.com/)
- [MacOSX](http://www.apple.com/osx/)
- [MacVim](https://github.com/macvim-dev/macvim)
- [Magic Launch](https://www.oneperiodic.com/products/magiclaunch/)
- [MagicPrefs](http://magicprefs.com/)
- [Maid](https://github.com/benjaminoakes/maid/)
- [Mailmate](http://freron.com/)
- [Mailplane](http://mailplaneapp.com/)
- [Marked 2](http://marked2app.com)
- [MATLAB](http://www.mathworks.com/products/matlab/)
- [Maven](http://maven.apache.org)
- [Max](http://sbooth.org/Max/)
- [MenuMeters](http://www.ragingmenace.com/software/menumeters/)
- [Mercurial](https://www.mercurial-scm.org/)
- [MercuryMover](http://www.heliumfoot.com/mercurymover/)
- [Messages](http://www.apple.com/osx/apps/#messages)
- [Micro](https://github.com/zyedidia/micro)
- [Microsoft Azure CLI](https://github.com/Azure/azure-xplat-cli)
- [Microsoft Remote Desktop](https://itunes.apple.com/us/app/microsoft-remote-desktop/id715768417?mt=12&ls=1)
- [MonoDevelop](http://www.monodevelop.com)
- [Moom](http://manytricks.com/moom/)
- [Mou](http://25.io/mou/)
- [mpd](http://www.musicpd.org)
- [MPlayerX](http://mplayerx.org)
- [MPS Youtube](https://github.com/mps-youtube/mps-youtube)
- [MPV](https://mpv.io/)
- [MusicBrainz Picard](https://picard.musicbrainz.org/)
- [myrepos](https://github.com/joeyh/myrepos)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)
- [MySQL](http://www.mysql.com/)
- [Name Mangler](http://manytricks.com/namemangler/)
- [Nano](http://www.nano-editor.org/)
- [Navicat](http://navicat.com/)
- [ncmpcpp](http://rybczak.net/ncmpcpp/)
- [neovim](https://github.com/neovim/neovim)
- [Nethack](http://www.nethack.org)
- [newsbeuter](http://newsbeuter.org/)
- [ngrok](https://ngrok.com/)
- [Nomacs](http://nomacs.org/)
- [npm](https://www.npmjs.com/)
- [nvALT](http://brettterpstra.com/projects/nvalt/)
- [nvpy](https://github.com/cpbotha/nvpy)
- [Oh My Fish](https://github.com/bpinto/oh-my-fish)
- [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)
- [OmniFocus](https://www.omnigroup.com/omnifocus/)
- [OmniGraffle](https://www.omnigroup.com/omnigraffle/)
- [Openbox](http://openbox.org)
- [OpenEmu](http://openemu.org)
- [OpenSSH](http://www.openssh.com/) (NOTE: includes private keys)
- [Paintbrush](http://paintbrush.sourceforge.net/)
- [Pandoc](http://pandoc.org)
- [Pass](http://www.passwordstore.org/)
- [Pastebot](http://tapbots.com/software/pastebot/)
- [Path Finder](http://www.cocoatech.com/pathfinder/)
- [Pear](http://pear.php.net/)
- [Pentadactyl](http://5digits.org/pentadactyl/)
- [Perl](https://www.perl.org/)
- [Phoenix](https://github.com/kasper/phoenix)
- [PhpStorm](http://www.jetbrains.com/phpstorm/)
- [Pidgin](https://www.pidgin.im)
- [PIP](http://www.pip-installer.org/)
- [Poedit](http://poedit.net/)
- [PokerStars](https://www.pokerstars.com/)
- [PopClip](http://pilotmoon.com/popclip/)
- [Popcorn-Time](https://popcorntime.io/)
- [PostgreSQL](http://www.postgresql.org/)
- [Postico](https://eggerapps.at/postico/)
- [Pow](http://pow.cx/)
- [Prezto](https://github.com/sorin-ionescu/prezto)
- [Processing](https://processing.org/)
- [ProxyChains NG](http://sourceforge.net/projects/proxychains-ng/)
- [ProxyChains](http://proxychains.sourceforge.net)
- [Punto Switcher](https://punto.yandex.ru/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [PyPI](https://pypi.python.org/pypi)
- [PyRadio](http://www.coderholic.com/pyradio/)
- [Querious](http://www.araelium.com/querious/)
- [Quicksilver](http://qsapp.com/)
- [Qutebrowser](http://qutebrowser.org/)
- [R](http://www.r-project.org/)
- [Rails](http://rubyonrails.org/)
- [Redshift Scheduler](https://github.com/spantaleev/redshift-scheduler)
- [Redshift](http://jonls.dk/redshift/)
- [Rhythmbox](https://wiki.gnome.org/Apps/Rhythmbox)
- [Rime](http://rime.im/)
- [Robomongo](http://robomongo.org/)
- [Royal TSX](http://www.royaltsx.com/ts/osx/features)
- [RStudio](https://www.rstudio.com/)
- [rTorrent](http://libtorrent.rakshasa.no/)
- [Rubocop](https://github.com/bbatsov/rubocop)
- [Ruby Version](https://gist.github.com/fnichol/1912050)
- [Ruby](https://www.ruby-lang.org/)
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
- [SecureCRT](https://www.vandyke.com/products/securecrt/)
- [Seil](https://pqrs.org/osx/karabiner/seil.html.en)
- [SelfControl](http://selfcontrolapp.com/)
- [Sequel Pro](http://www.sequelpro.com/)
- [ShiftIt](https://github.com/fikovnik/ShiftIt)
- [Shimo](https://www.feingeist.io/shimo/)
- [ShowyEdge](https://pqrs.org/osx/ShowyEdge/index.html.en)
- [SHSH Blobs](https://en.wikipedia.org/wiki/SHSH_blob)
- [Shuttle](http://fitztrev.github.io/shuttle/)
- [SizeUp](http://www.irradiatedsoftware.com/sizeup/)
- [Sketch](http://sketchapp.com/)
- [Skim](http://skim-app.sourceforge.net/)
- [Skitch](https://evernote.com/skitch/)
- [Slate](https://github.com/jigish/slate)
- [Slic3r](http://slic3r.org)
- [Slogger](http://brettterpstra.com/projects/slogger/)
- [SmartGit](http://www.syntevo.com/smartgit/)
- [Smooth Mouse](http://smoothmouse.com/)
- [Soulver](http://www.acqualia.com/soulver/)
- [SourceTree](https://www.sourcetreeapp.com/)
- [Spacemacs](https://github.com/syl20bnr/spacemacs)
- [Spark](http://www.shadowlab.org/softwares/spark.php)
- [Spectacle](https://www.spectacleapp.com/)
- [Spectrwm](https://github.com/conformal/spectrwm/wiki)
- [Splice](https://splice.com/)
- [Spotify Notifications](http://spotify-notifications.citruspi.io/)
- [Spotify](https://www.spotify.com/)
- [Stata](http://www.stata.com/)
- [Stay](https://cordlessdog.com/stay/)
- [Sublime Text](http://www.sublimetext.com/)
- [Subversion](http://subversion.apache.org/)
- [SuperDuper!](http://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html)
- [Surge](http://surge.run/manual/)
- [Swinsian](http://swinsian.com/)
- [T](http://sferik.github.io/t/)
- [TaskPaper](http://www.hogbaysoftware.com/products/taskpaper)
- [Taskwarrior](http://taskwarrior.org/)
- [Teamocil](http://remiprev.github.io/teamocil/)
- [Telegram for macOS](https://macos.telegram.org)
- [Terminal](http://www.apple.com/osx/apps/)
- [Terminator](https://launchpad.net/terminator/)
- [TextExpander](https://smilesoftware.com/textexpander)
- [TextMate](http://macromates.com/)
- [Textual](http://www.codeux.com/textual/)
- [Tig](https://github.com/jonas/tig)
- [tint2](https://code.google.com/p/tint2/)
- [TinyFugue](http://tinyfugue.sourceforge.net)
- [Tmux](http://tmux.sourceforge.net/)
- [Tmuxp](https://github.com/tony/tmuxp)
- [Tmuxinator](https://github.com/tmuxinator/tmuxinator)
- [Todo.txt CLI](http://todotxt.com/)
- [TotalSpaces2](http://totalspaces.binaryage.com/)
- [Tower](http://www.git-tower.com/)
- [Transmission](http://www.transmissionbt.com/)
- [Transmit](http://panic.com/transmit/)
- [Tunnelblick](https://tunnelblick.net)
- [tvnamer](https://github.com/dbr/tvnamer)
- [Twitterrific](http://twitterrific.com/)
- [Typinator](http://www.ergonis.com/products/typinator/)
- [uTorrent](http://www.utorrent.com/)
- [Ventrilo](http://www.ventrilo.com/)
- [Versions](http://www.versionsapp.com)
- [Vim](http://www.vim.org/)
- [Vimperator](http://www.vimperator.org/vimperator)
- [Viscosity](http://www.sparklabs.com/viscosity/)
- [Visual Studio Code - Insiders](https://code.visualstudio.com)
- [Visual Studio Code](https://code.visualstudio.com)
- [VLC](http://www.videolan.org/)
- [Wakatime](https://wakatime.com/)
- [WebStorm](https://www.jetbrains.com/webstorm/)
- [Wget](https://www.gnu.org/software/wget/)
- [WhatsApp Web](https://web.whatsapp.com/)
- [Wireshark 2](https://www.wireshark.org)
- [Witch](http://manytricks.com/witch/)
- [WordPress WP-CLI](http://wp-cli.org/)
- [Workrave](http://www.workrave.org/)
- [X11](http://www.x.org/)
- [Xamarin Studio](https://xamarin.com/studio)
- [XBindKeys](http://www.nongnu.org/xbindkeys/)
- [Xchat](http://xchat.org/)
- [Xcode](https://developer.apple.com/xcode/)
- [XEmacs](http://www.xemacs.org/)
- [XLD](http://tmkk.undo.jp/xld/)
- [XtraFinder](http://www.trankynam.com/xtrafinder/)
- [Yummy FTP](http://www.yummysoftware.com/)
- [z](https://github.com/rupa/z)
- [zathura](https://pwmt.org/projects/zathura/)
- [Zsh](http://zsh.sourceforge.net/)
- [Übersicht](http://tracesof.net/uebersicht/)
- iTunes Applescripts

## Can you support application X

We can [with your help](doc#get-official-support-for-an-application) ;)

## Personalization & configuration

Have an application that shouldn't be generally supported but that you use?
Or a cool file you want to sync?

- Use a `~/.mackup.cfg` to [sync a single file](doc#configuration) (e.g. `~/.gitignore`)
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
