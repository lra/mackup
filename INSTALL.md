# Detailled install instructions for Mackup

There are 3 ways to run mackup

1. Install it with Homebrew and run it (OSX only)
1. Download it, install it with python setuptools and run it (OSX and
   GNU/Linux)
1. Download it, and run it without installing it (OSX and GNU/Linux)

## Install

### With Homebrew (OSX only)

```bash
# Easy
brew install mackup

# Now just run it
mackup -h
```

### With Python Setuptools

```bash
# Download Mackup
curl -o mackup.zip https://codeload.github.com/lra/mackup/zip/master

# Uncompress the archive
unzip mackup.zip

# Install Mackup on your system
cd mackup-master
sudo python setup.py install

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

### With Python Setuptools

```bash
# Download Mackup
curl -o mackup.zip https://codeload.github.com/lra/mackup/zip/master

# Uncompress the archive
unzip mackup.zip

# Install Mackup on your system
cd mackup-master
sudo python setup.py install

# Now you can run it
mackup -h
```

## Uninstall

### With Homebrew (OSX only)

```bash
brew uninstall mackup
```

### With Python Setuptools

```bash
sudo rm -rf /usr/local/bin/mackup /usr/local/lib/python?.?/site-packages/Mackup-*.egg/
```


