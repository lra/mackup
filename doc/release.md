# Release

Releasing is now automated. Pushing a version tag triggers the
[`release` workflow](../.github/workflows/release.yaml), which builds the
package, publishes it to PyPI, and creates the GitHub release.

To cut a release, run one command. The version is `X.Y.Z`
(`major.minor.patch`), and the `BUMP` you choose increments one number and
resets the numbers to its right to `0`:

```sh
make release              # patch: 0.10.3 -> 0.10.4 (bug fixes)
make release BUMP=minor   # minor: 0.10.3 -> 0.11.0 (new features)
make release BUMP=major   # major: 0.10.3 -> 1.0.0  (breaking changes)
make release VERSION=1.2.3  # pin an exact version, no arithmetic
```

Preview a bump without changing anything with `uv version --bump <level>
--dry-run`.

This runs the checks, bumps the version, syncs the lockfile, then commits, tags
and pushes. The workflow takes over from the tag push:

- Builds the package with `uv build`
- Publishes it to PyPI with `uv publish`
- Creates the GitHub release with auto-generated notes and the built artifacts
