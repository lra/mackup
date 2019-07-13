# How to contribute

You can:

- Add or improve the support of an application (Check the [TODO][TODO] and
  [TOFIX][TOFIX] tasks and pick one)
- Improve the Mackup codebase
- You can triage issues which may include reproducing bug reports or asking for
  vital information, such as version numbers or reproduction instructions. If
  you would like to start triaging issues, one easy way to get started is to
  [subscribe to mackup on CodeTriage](https://www.codetriage.com/lra/mackup).
  [![Open Source Helpers][CODETRIAGE-IMG]][CODETRIAGE]

To speed up Pull Request (PR) approval and merger into Mackup, please follow
these guidelines:

- Keep one application supported per PR
- Add the application to the list of supported applications in
  [README.md](README.md)
- Add your change to the WIP section of the [CHANGELOG.md](CHANGELOG.md)
- Sync configurations should follow the following principles:
  - Syncing should not break the application, and PRs should be tested
  - Syncing should not break any syncing functionality internal to the
    application
  - The configuration should sync the minimal set of data, so that syncing
    happens quickly. Leave large app data out of the sync configuration.
  - Do not sync any file or folder that represents some state, like session
    data, cache, any file specific to the local workstation.
  - Do not sync sensitive information, like clear passwords or private keys

Thank you for your contribution!

[TODO]: https://github.com/lra/mackup/labels/TODO
[TOFIX]: https://github.com/lra/mackup/labels/TOFIX
[CODETRIAGE]: https://www.codetriage.com/lra/mackup
[CODETRIAGE-IMG]: https://www.codetriage.com/lra/mackup/badges/users.svg
