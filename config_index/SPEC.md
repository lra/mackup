# Application Configuration Index Specification

**Version:** 1.0.0

This document specifies the format and structure of the application configuration index used for syncing application settings to cloud storage (S3, R2, etc.).

## Overview

The configuration index provides a comprehensive database of file paths where applications store their configuration data. This enables sync engines to:

1. Discover which files to backup for each application
2. Handle platform-specific paths (macOS vs Linux)
3. Support XDG Base Directory specification on Linux

## Index Format

### Primary Format: JSON

**File:** `application_configs.json`

```json
{
  "metadata": {
    "source": "string",
    "source_url": "string",
    "total_applications": "number",
    "total_home_paths": "number",
    "total_xdg_paths": "number",
    "total_macos_library_paths": "number",
    "description": "string"
  },
  "path_resolution": {
    "home_relative": "string",
    "xdg_relative": "string",
    "macos_library": "string"
  },
  "applications": {
    "<app_id>": {
      "name": "string",
      "config_file": "string",
      "configuration_files": ["string"],
      "xdg_configuration_files": ["string"]
    }
  },
  "all_paths": {
    "home_relative": ["string"],
    "xdg_relative": ["string"],
    "macos_library_only": ["string"]
  }
}
```

## Schema Definitions

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Origin of the configuration data |
| `source_url` | string | URL to the source repository |
| `total_applications` | number | Total count of indexed applications |
| `total_home_paths` | number | Count of home-relative paths |
| `total_xdg_paths` | number | Count of XDG-relative paths |
| `total_macos_library_paths` | number | Count of macOS Library paths |
| `description` | string | Human-readable description |

### Application Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable application name |
| `config_file` | string | Source config filename (e.g., `git.cfg`) |
| `configuration_files` | string[] | Paths relative to `$HOME` |
| `xdg_configuration_files` | string[] | Paths relative to `$XDG_CONFIG_HOME` |

## Path Resolution

### Home-Relative Paths

Paths in `configuration_files` are relative to the user's home directory.

```
~/.gitconfig     → $HOME/.gitconfig
Library/Prefs/x  → $HOME/Library/Prefs/x (macOS only)
```

### XDG Paths

Paths in `xdg_configuration_files` are relative to `$XDG_CONFIG_HOME`.

```
nvim/init.lua → $XDG_CONFIG_HOME/nvim/init.lua
              → ~/.config/nvim/init.lua (default)
```

**XDG Resolution:**
```typescript
const xdgHome = process.env.XDG_CONFIG_HOME || join(homedir(), '.config');
const fullPath = join(xdgHome, relativePath);
```

### Platform Filtering

Paths starting with `Library/` are macOS-specific and should be skipped on Linux:

```typescript
function shouldSync(path: string, platform: string): boolean {
  if (platform === 'linux' && path.startsWith('Library/')) {
    return false;
  }
  return true;
}
```

## Application ID Convention

Application IDs (`<app_id>`) follow these conventions:

- Lowercase alphanumeric with hyphens
- Derived from the source config filename without `.cfg` extension
- Examples: `git`, `vscode`, `jetbrains-idea`, `1password-4`

## Alternative Formats

### YAML Format

**File:** `application_configs.yaml`

Human-readable format with the same structure as JSON.

### Flat Text Format

**File:** `all_paths.txt`

Simple line-based format for shell scripts:

```
# Format: [APP_ID] PATH

## Home-relative paths (relative to ~)
[git] ~/.gitconfig
[bash] ~/.bashrc

## XDG paths (relative to $XDG_CONFIG_HOME)
[nvim] $XDG_CONFIG_HOME/nvim/init.lua
```

## Usage Examples

### Load Index (TypeScript/Bun)

```typescript
const index = await Bun.file('application_configs.json').json();
```

### Get Paths for Application

```typescript
function getAppPaths(appId: string): string[] {
  const app = index.applications[appId];
  if (!app) return [];

  const home = homedir();
  const xdgHome = process.env.XDG_CONFIG_HOME || join(home, '.config');
  const paths: string[] = [];

  for (const p of app.configuration_files) {
    paths.push(join(home, p));
  }

  for (const p of app.xdg_configuration_files) {
    paths.push(join(xdgHome, p));
  }

  return paths;
}
```

### Filter for Platform

```typescript
function getAppPathsForPlatform(appId: string, platform: 'darwin' | 'linux'): string[] {
  return getAppPaths(appId).filter(path => {
    if (platform === 'linux' && path.includes('/Library/')) {
      return false;
    }
    return true;
  });
}
```

## Versioning

The index format follows semantic versioning:

- **Major:** Breaking changes to schema structure
- **Minor:** New fields added (backward compatible)
- **Patch:** Data updates, bug fixes

Current applications are sourced from Mackup v0.8.43 application database.

## Regenerating the Index

```bash
cd scripts
bun run generate
```

This parses all `.cfg` files and regenerates the JSON, YAML, and TXT outputs.
