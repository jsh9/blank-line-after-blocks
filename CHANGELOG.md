# Change Log

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2025-09-03

- Changed
  - Formatter no longer inserts a blank line before the second part of compound
    blocks (`else/elif/except/finally`). This avoids awkward spacing like a
    blank line before `else:` and keeps compound statements visually tight.
- Added
  - `--version` flag for both CLIs (`blank-line-after-blocks` and
    `blank-line-after-blocks-jupyter`) to print the tool version.
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/0.1.3...0.1.4

## [0.1.3] - 2025-09-02

- Fixed
  - Exclude functionality now works correctly for single files in pre-commit
    hooks
- Added
  - Tests for single file exclusion scenarios
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/0.1.2...0.1.3

## [0.1.2] - 2025-09-01

- Added
  - A config option `--exclude` to exclude certain directories/files
- Removed
  - An unnecessary config option `--exit-zero-even-if-changed`
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/0.1.1...0.1.2

## [0.1.1] - 2025-08-27

- Changed
  - Refactor code & add test cases
- Fixed
  - File path for Windows
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/0.1.0...0.1.1

## [0.1.0] - 2025-08-27

- Added
  - Initial release of blank-line-after-blocks formatter
  - Core functionality to add blank lines after code blocks (if, for, while,
    with, try/except, etc.)
  - Support for Python (.py) files
  - Support for Jupyter notebooks (.ipynb)
  - Command-line interface for processing files and directories
  - Pre-commit hook integration
  - Comprehensive test suite with test data for various scenarios
  - Configuration support via pyproject.toml and tox.ini
  - Development dependencies and tooling setup
- Full diff
  - N/A
