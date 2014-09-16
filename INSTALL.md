# Detailled install instructions for Mackup

There are 3 ways to run mackup

1. Install it with Homebrew (OSX only)
1. Install it with PIP (OSX and GNU/Linux)
1. Download it, and run it without installing it (OSX and GNU/Linux)

## Install

### With Homebrew (OSX only)

```bash
# Easy
brew install mackup

# Now just run it
mackup -h
```

### With Python's PIP

```bash
# Easy too
pip install mackup

# Now you can run it
mackup -h
```

### Run it without installing it

```bash
# Download Mackup
curl -o mackup.zip https://codeload.github.com/lra/mackup/zip/master

# Uncompress the archive
unzip mackup.zip

# Run it without the need to install it
./mackup-master/bin/mackup -h
```

## Upgrade

### With Homebrew (OSX only)

```bash
brew update
brew upgrade
mackup -h
```

### With Python's PIP

```bash
pip install --upgrade mackup
mackup -h
```

## Uninstall

### With Homebrew (OSX only)

```bash
brew uninstall mackup
```

### With Python's PIP

```bash
pip uninstall mackup
```


