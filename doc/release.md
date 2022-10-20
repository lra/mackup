# Release

1. Move all the WIP changes under a new version in the [changelog](../CHANGELOG.md)
2. Increment the version in [constants.py](../mackup/constants.py)
3. `git commit` with the message `Mackup X.Y.Z`
4. `git tag <version>`
5. `git push`
6. `git push --tags`
7. `make release`
