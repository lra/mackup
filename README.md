# Application Configuration Index

A comprehensive index of application configuration file locations for use with custom sync engines (S3, R2, etc.).

## Overview

This repository provides a structured database of where 581+ applications store their configuration files on macOS and Linux. Use this index to build backup/sync tools that preserve your application settings.

## Quick Start

```typescript
// Load the index
const index = await Bun.file('config_index/application_configs.json').json();

// Get all paths for an application
const app = index.applications['git'];
console.log(app.configuration_files);
// [".gitconfig"]
console.log(app.xdg_configuration_files);
// ["git/config", "git/ignore", "git/attributes"]
```

## Index Contents

| File | Format | Use Case |
|------|--------|----------|
| `application_configs.json` | JSON | Programmatic access |
| `application_configs.yaml` | YAML | Human-readable |
| `all_paths.txt` | Plain text | Shell scripts, quick reference |
| `SPEC.md` | Markdown | Format specification |

## Statistics

| Metric | Count |
|--------|-------|
| Applications | 581 |
| Home-relative paths | 1,307 |
| XDG paths | 196 |
| macOS Library paths | 884 |

## Path Types

### Home-Relative Paths

Traditional dotfiles relative to `$HOME`:

```
.gitconfig      → ~/.gitconfig
.bashrc         → ~/.bashrc
.config/nvim    → ~/.config/nvim
```

### XDG Paths

Linux paths following XDG Base Directory spec, relative to `$XDG_CONFIG_HOME` (defaults to `~/.config`):

```
nvim/init.lua   → ~/.config/nvim/init.lua
git/config      → ~/.config/git/config
```

### macOS Library Paths

macOS-specific paths (skip on Linux):

```
Library/Application Support/Code/User/settings.json
Library/Preferences/com.apple.Terminal.plist
```

## Regenerating the Index

If you need to update the index from the source configs:

```bash
cd scripts
bun run generate
```

## Example: Sync Engine Integration

```typescript
import { homedir } from 'os';
import { join } from 'path';

interface ConfigIndex {
  applications: Record<string, {
    name: string;
    configuration_files: string[];
    xdg_configuration_files: string[];
  }>;
}

async function getPathsToSync(appIds: string[]): Promise<string[]> {
  const index: ConfigIndex = await Bun.file('config_index/application_configs.json').json();
  const home = homedir();
  const xdgHome = process.env.XDG_CONFIG_HOME || join(home, '.config');
  const platform = process.platform;
  const paths: string[] = [];

  for (const appId of appIds) {
    const app = index.applications[appId];
    if (!app) continue;

    // Home-relative paths
    for (const p of app.configuration_files) {
      // Skip macOS Library paths on Linux
      if (platform === 'linux' && p.startsWith('Library/')) continue;
      paths.push(join(home, p));
    }

    // XDG paths
    for (const p of app.xdg_configuration_files) {
      paths.push(join(xdgHome, p));
    }
  }

  return paths;
}

// Usage
const paths = await getPathsToSync(['git', 'bash', 'nvim', 'vscode']);
// Sync these paths to S3/R2...
```

## Application Categories

### Development

`git`, `nvim`, `vscode`, `vim`, `emacs`, `sublime-text`, `jetbrains-*`

### Shell & Terminal

`bash`, `zsh`, `fish`, `tmux`, `alacritty`, `kitty`, `iterm2`

### Cloud & DevOps

`aws`, `azure`, `gcloud`, `docker`, `kubernetes`, `terraform`, `ansible`

### System Utilities

`homebrew`, `karabiner`, `alfred`, `hammerspoon`, `i3`, `sway`, `rofi`

## Source

Configuration data extracted from [Mackup](https://github.com/lra/mackup) application database (v0.8.43).

## License

GPL-3.0 (inherited from Mackup)
