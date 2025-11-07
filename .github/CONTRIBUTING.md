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

## Development Setup

Mackup uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management. Here's how to get started:

### Prerequisites

- Python 3.9 or higher
- [uv](https://docs.astral.sh/uv/) installed

Install uv if you haven't already:

```bash
# On macOS
brew install uv

# On Linux
# Via pipx (recommended)
pipx install uv

# Or via Homebrew on Linux
brew install uv

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively, see the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more options.

### Setting Up Your Development Environment

1. Clone the repository:

```bash
git clone https://github.com/lra/mackup.git
cd mackup
```

2. Sync dependencies (creates a virtual environment automatically):

```bash
uv sync --dev
```

This will:
- Create a `.venv` directory with a virtual environment
- Install all project dependencies
- Install development dependencies (pytest, mypy, etc.)

### Running Tests and Checks

Use the provided Make targets for quick development workflow:

```bash
# Run all checks (recommended before committing)
make check

# Run tests only
make test

# Run type checking
make mypy

# Run code linting
make ruff
```

Or use `uv run` directly:

```bash
# Run tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run type checking
uv run mypy mackup/

# Run linting
ruff check .
```

### Code Quality Standards

All pull requests must pass:
- ✅ **Tests**: All pytest tests must pass
- ✅ **Type checking**: No mypy errors
- ✅ **Linting**: Code must pass ruff checks
- ✅ **Formatting**: Follow existing code style

Run `make check` before submitting your PR to ensure everything passes.

## Contributing Guidelines

To speed up Pull Request (PR) approval and merger into Mackup, please follow
these guidelines:

- Keep one application supported per PR
- Add the application to the list of supported applications in
  [README.md][README.md]
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
[README.md]: https://github.com/lra/mackup/blob/master/README.md
