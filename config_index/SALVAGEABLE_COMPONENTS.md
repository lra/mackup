# Salvageable Components from Mackup

This document identifies valuable components from Mackup that can be reused
for custom sync engines (e.g., S3-based snapshot systems).

## 1. Application Configuration Index

**Location:** `config_index/application_configs.json`

### Summary
| Metric | Count |
|--------|-------|
| Total Applications | 581 |
| Home-relative Paths | 1,307 |
| XDG Paths | 196 |
| macOS Library Paths | 884 |

### Path Types

1. **Home-relative paths** (`~/.bashrc`, `~/.gitconfig`)
   - Traditional dotfiles in home directory
   - Cross-platform (macOS/Linux)

2. **XDG paths** (`$XDG_CONFIG_HOME/nvim/`)
   - Linux-focused, follows XDG Base Directory spec
   - Default: `~/.config/`
   - Override via `$XDG_CONFIG_HOME` env var

3. **macOS Library paths** (`~/Library/Application Support/...`)
   - macOS-specific application data
   - Includes `.plist` preference files
   - Skip these on Linux

---

## 2. Utility Functions Worth Salvaging

### File Operations (`mackup/utils.py`)

```python
# Safe file deletion with ACL/attribute handling
def delete(filepath):
    remove_acl(filepath)           # Remove access control lists
    remove_immutable_attribute(filepath)  # Remove immutable flags
    # Then delete file/dir/link

# Recursive copy with proper permissions
def copy(src, dst):
    # Creates parent dirs if needed
    # Sets secure permissions (600 files, 700 dirs)

# Symlink creation
def link(target, link_to):
    # Creates parent dirs if needed
    # Sets proper permissions before linking
```

### Platform-Specific Handlers

```python
# ACL removal (different on macOS vs Linux)
def remove_acl(path):
    # macOS: /bin/chmod -R -N
    # Linux: /bin/setfacl -R -b

# Immutable attribute removal
def remove_immutable_attribute(path):
    # macOS: /usr/bin/chflags -R nouchg
    # Linux: /usr/bin/chattr -R -f -i

# Platform-aware path filtering
def can_file_be_synced_on_current_platform(path):
    # Skips ~/Library/* on Linux
```

### Storage Detection (`mackup/utils.py`)

```python
# Auto-detect cloud storage locations
def get_dropbox_folder_location():
    # Reads ~/.dropbox/host.db (base64 encoded path)

def get_google_drive_folder_location():
    # Queries sync_config.db SQLite database

def get_icloud_folder_location():
    # Uses ~/Library/Mobile Documents/com~apple~CloudDocs/
```

---

## 3. Configuration Database Logic (`mackup/appsdb.py`)

### Key Features to Salvage:

1. **INI Parser with case preservation**
   ```python
   config = configparser.ConfigParser(allow_no_value=True)
   config.optionxform = str  # Preserve original case of paths
   ```

2. **XDG path resolution**
   ```python
   xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
   # Paths in [xdg_configuration_files] are relative to this
   ```

3. **Custom app override support**
   - User configs in `~/.mackup/*.cfg` override built-in ones
   - Allows adding custom applications without modifying source

---

## 4. Application Profile Logic (`mackup/application.py`)

### Backup/Restore Algorithms

**Backup Algorithm:**
```
for each config_file:
    if exists(~/config_file) AND not already_symlinked:
        copy(~/config_file → backup/config_file)
        delete(~/config_file)
        symlink(backup/config_file → ~/config_file)
```

**Restore Algorithm:**
```
for each config_file:
    if exists(backup/config_file) AND not already_symlinked:
        if exists(~/config_file):
            prompt_to_replace()
        symlink(backup/config_file → ~/config_file)
```

**For S3 Snapshot Engine:** You don't need symlinks. Simplify to:
```
for each config_file:
    if exists(~/config_file):
        snapshot to S3 with metadata (timestamp, machine_id)
```

---

## 5. Index Files Generated

| File | Format | Use Case |
|------|--------|----------|
| `application_configs.json` | JSON | Programmatic access, S3 sync engine |
| `application_configs.yaml` | YAML | Human-readable, config management |
| `all_paths.txt` | Plain text | Quick reference, shell scripts |

---

## 6. Application Categories (Examples)

### Development Tools
- **Editors:** vim, neovim, emacs, vscode, sublime-text, atom
- **IDEs:** jetbrains-*, androidstudio, xcode
- **Version Control:** git, mercurial, subversion
- **Package Managers:** npm, yarn, pip, cargo, homebrew

### Shell & Terminal
- **Shells:** bash, zsh, fish, tcsh, ksh
- **Multiplexers:** tmux, screen
- **Terminals:** alacritty, iterm2, kitty, hyper

### Cloud & DevOps
- **Cloud CLI:** aws, azure, gcloud, heroku
- **Containers:** docker, lazydocker, kubernetes
- **IaC:** terraform, ansible, chef, puppet

### System Utilities
- **macOS:** bartender, alfred, karabiner, hammerspoon
- **Linux:** i3, sway, rofi, polybar

---

## 7. Recommended Usage for S3 Sync Engine

```typescript
import { homedir } from 'os';
import { join } from 'path';

// Load the index
const index = await Bun.file('config_index/application_configs.json').json();

// Get paths for specific apps
function getPathsForApp(appId: string): string[] {
  const app = index.applications[appId];
  if (!app) return [];

  const paths: string[] = [];
  const home = homedir();

  // Home-relative paths
  for (const p of app.configuration_files) {
    paths.push(join(home, p));
  }

  // XDG paths
  const xdgHome = process.env.XDG_CONFIG_HOME || join(home, '.config');
  for (const p of app.xdg_configuration_files) {
    paths.push(join(xdgHome, p));
  }

  return paths;
}

// Example: Get all git config paths
const gitPaths = getPathsForApp('git');
// Returns: ['~/.gitconfig', '~/.config/git/config', '~/.config/git/ignore', ...]
```

---

## 8. Files to Copy for Your Sync Engine

```
config_index/
├── application_configs.json  # Primary index
├── application_configs.yaml  # Alternative format
├── all_paths.txt             # Quick reference
└── SALVAGEABLE_COMPONENTS.md # This document

scripts/
├── package.json              # Bun project config
├── tsconfig.json             # TypeScript config
├── generate-config-index.ts  # Main generator script
└── lib/
    └── ini-parser.ts         # INI file parser

mackup/utils.py               # Useful utility functions (copy selectively)
```

### Regenerating the Index

```bash
cd scripts
bun install        # Install dependencies (optional, only for types)
bun run generate   # Regenerate the index
```

---

## 9. Not Worth Salvaging

- **Symlink logic** - S3 snapshots don't need symlinks
- **Interactive prompts** - CLI confirmations not needed for automated sync
- **Storage engine detection** - You're using S3, not Dropbox/iCloud
- **Config file parsing** - You'll define your own config format

---

## 10. License Note

Mackup is GPL-3.0 licensed. If you're incorporating code directly,
ensure compliance. The **application configuration data** (list of paths)
is factual information about where apps store configs, which is generally
not copyrightable.
