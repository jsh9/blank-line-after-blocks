# Change Log

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-09-01

- Added
  - A config option `--exclude` to exclude certain directories/files
- Removed
  - An unnecessary config option `--exit-zero-even-if-changed`
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/v0.1.1...v0.1.2

## [0.1.1] - 2025-08-27

- Changed
  - Refactor code & add test cases
- Fixed
  - File path for Windows
- Full diff
  - https://github.com/jsh9/blank-line-after-blocks/compare/v0.1.0...v0.1.1

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
