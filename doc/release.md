# Release

Releasing is now automated. Pushing a version tag triggers the
[`release` workflow](../.github/workflows/release.yaml), which builds the
package, publishes it to PyPI, and creates the GitHub release.

To cut a release:

1. Increment the version in [pyproject.toml](../pyproject.toml)
1. Run `uv sync -U`
1. `git commit` with the message `Mackup X.Y.Z`
1. `git tag X.Y.Z`
1. `git push && git push --tags`

That's it. The workflow takes over from the tag push:

- Builds the package with `uv build`
- Publishes it to PyPI with `uv publish`
- Creates the GitHub release with auto-generated notes and the built artifacts
