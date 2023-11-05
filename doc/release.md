# Release

1. Move all the WIP changes under a new version in the [changelog](../CHANGELOG.md)
1. Increment the version in [constants.py](../mackup/constants.py)
1. Increment the version in [pyproject.toml](../pyproject.toml)
1. `git commit` with the message `Mackup X.Y.Z`
1. `git tag <version>`
1. `git push`
1. `git push --tags`
1. `make release`
