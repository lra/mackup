# How to contribute

To speed up Pull Request (PR) approval and merger into Mackup, please follow these guidelines:
- Keep one application supported per PR
- Add the application to the list of supported applications in README.md
- Add your change to the WIP section of CHANGELOG.md
- Sync configurations should follow the follow principles:
  - Syncing should not break the application, and PRs should be tested
  - Syncing should not break any syncing functionality internal to the application
  - The configuation should sync the minimal set of data, so that syncing happens quickly. Leave large app data out of the sync configuration.

Thank you for your contribution!
