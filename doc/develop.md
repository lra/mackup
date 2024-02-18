# Develop

```sh
# Install a recent non-system python
brew install python

# Install pipx to be able to easily run isolated Python packages
brew install pipx

# Install the tool for dependency management and packaging in Python
pipx install poetry

# Setup local dev
cd .../mackup
poetry install --with dev

# You can now edit files and see the impact of your changes
poetry run mackup --version
make test
```
