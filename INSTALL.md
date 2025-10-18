# Detailed install instructions for Mackup

There are 2 ways to run mackup:

1. Install it with Homebrew (OSX only)
2. Install it with PIP (OSX and GNU/Linux)

## Install

### With Homebrew (OSX only)

```bash
# Easy
brew install mackup

# Now just run it
mackup -h
```

### With Homebrew (OSX only) master branch for latest updates

Want to install the latest master release instead of waiting on the homebrew
package version?

[Homebrew reference](https://docs.brew.sh/Manpage#install-options-formulacask)

```bash
# Install master
brew install --HEAD
# Check if you are using the master or stale package
brew switch mackup <HEAD-XXXX>

mackup -h
```

### With Python's PIP

```bash
# Easy too
pip install mackup

# Now you can run it
mackup -h
```

## Upgrade

### Upgrade with Homebrew (OSX only)

```bash
brew update
brew upgrade
mackup -h
```

### Upgrade with Python's PIP

```bash
pip install --upgrade mackup
mackup -h
```

## Uninstall

### Uninstall with Homebrew (OSX only)

```bash
brew uninstall mackup
```

### Uninstall with Python's PIP

```bash
pip uninstall mackup
```
