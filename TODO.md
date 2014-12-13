# TODO

Feel free to implement any of those ;)

- `mackup status` to display any synced app, and any app that could be synced
  by launching `mackup backup`
- A GUI, we could definitely use an OS X gui that would display the status:
  synced apps, unsynced apps, using wxPython ?
- Try with hard links to support the Fonts pb
- 100% test coverage
- Rollback any file that's not maintained by mackup anymore
  https://github.com/lra/mackup/issues/190
- Ability to encrypt specific files, asked in #134 and #109
- Setup some webpage
- Ability to enable/disable an app (will update the cfg file)
- Progress bar on syncing
- Invite the user to generate the conf file at launch if Mackup has no conf
  file
- Merge all the config code in Config()
- Ability to `mackup list` without any storage, and use `mackup list` as a test
  in `homebrew`
- Do not crash on non existing file during uninstall #240
- Simplify the parameter handling with https://github.com/mitsuhiko/click
