# Develop

```sh
# Install a recent non-system python
brew install python

# Install pyenv to be able to easily switch Python versions
brew install pyenv

# Install the package and virtualenv manager
brew install pipenv

# Install the most recent Python
pyenv install 3.7.4

# Setup local dev
cd .../mackup
pyenv local 3.7.4
pipenv install
pipenv shell
make develop

# You can now edit files and see the impact of your changes
mackup --version
nosetests

# Cleanup
make undevelop
```
