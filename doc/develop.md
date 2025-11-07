# Develop

```sh
# Install the tool for dependency management and packaging in Python
pipx install uv

# You can now edit files and see the impact of your changes
uv run mackup --version
make test
```

## Running Tests with Coverage

To run tests with coverage reporting:

```sh
# Run tests with coverage
make coverage

# View coverage report in terminal
make coverage-report

# Open HTML coverage report
open htmlcov/index.html
```

## Code Quality Checks

The project includes several code quality tools:

```sh
# Run all checks (ruff, mypy, pytest)
make check

# Run individual checks
make ruff      # Code linting
make mypy      # Type checking
make test      # Unit tests
make coverage  # Tests with coverage
```

## Coverage Configuration

Coverage is configured in `pyproject.toml` with:

- Branch coverage enabled
- Test files excluded from coverage
- HTML and XML reports generated
- 67%+ coverage currently achieved

The coverage reports are automatically uploaded to Codecov on CI runs for
Python 3.12.
