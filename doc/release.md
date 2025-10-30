# Release

1. Increment the version in [pyproject.toml](../pyproject.toml)
1. Run `uv sync -U`
1. `git commit` with the message `Mackup X.Y.Z`
1. `git tag <version>`
1. `git push`
1. `git push --tags`
1. Do a release at <https://github.com/lra/mackup/releases>
1. `make release`
