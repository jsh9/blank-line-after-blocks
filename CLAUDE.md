# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

This is a Python formatter called `blank-line-after-blocks` that automatically
adds blank lines after if/for/while/with/try blocks to improve code
readability. The project supports both Python source files (.py) and Jupyter
notebooks (.ipynb).

## Commands

### Testing

- Run all tests: `python -m pytest tests/ -v`
- Run specific test files:
  - `python -m pytest tests/test_helper.py -v`
  - `python -m pytest tests/test_main_py.py -v`
  - `python -m pytest tests/test_base_fixer.py -v`
  - `python -m pytest tests/test_main_jupyter.py -v`
  - `python -m pytest tests/test_integration.py -v`
  - `python -m pytest tests/test_end_to_end.py -v`
- Run with coverage:
  `python -m pytest tests/ --cov=blank_line_after_blocks --cov-report=term-missing`
- Run tox for multi-environment testing: `tox`

### Code Quality

- Type checking: `mypy blank_line_after_blocks/`
- Format code: `muff format --config=muff.toml blank_line_after_blocks tests`
- Check formatting (without modifying):
  `muff format --diff --config=muff.toml blank_line_after_blocks tests`
- Linting: `flake8 .`
- Pre-commit hooks: `pre-commit run -a`

### Manual Tool Testing

- Format Python files: `blank-line-after-blocks file1.py file2.py`
- Format with exclusions:
  `blank-line-after-blocks --exclude "tests/|_generated\.py$" src/`
- Format Jupyter notebooks: `blank-line-after-blocks-jupyter notebook.ipynb`

## Architecture

### Core Components

1. **Base Architecture**: Uses inheritance with `BaseFixer` as the base class
   that handles common file processing logic

   - `BaseFixer` (base_fixer.py): Abstract base class for file processing and
     exclusion logic
   - `PythonFileFixer` (main_py.py): Concrete implementation for Python source
     files
   - `JupyterFileFixer` (main_jupyter.py): Concrete implementation for Jupyter
     notebooks

1. **Core Logic**: The actual formatting logic is in `helper.py` with the
   `fix_src()` function that processes Python source code

1. **Configuration**: File exclusion patterns handled in `config.py` using
   regex matching

1. **Entry Points**: Two CLI commands defined in pyproject.toml:

   - `blank-line-after-blocks` → `main_py:main`
   - `blank-line-after-blocks-jupyter` → `main_jupyter:main`

### Key Design Patterns

- **Template Method Pattern**: `BaseFixer` defines the file processing
  workflow, subclasses implement `fix_one_file()`
- **Strategy Pattern**: Different fixers for Python files vs Jupyter notebooks
- **Single Responsibility**: Each module has a clear focus (config, helpers,
  file processing)

### Dependencies

- `click` for CLI interface
- `jupyter-notebook-parser>=0.1.4` for Jupyter notebook processing
- Development dependencies include pytest, mypy, pre-commit, tox

## Configuration

The tool supports exclusion patterns via:

1. CLI `--exclude` flag (takes precedence)
1. `pyproject.toml` configuration:
   ```toml
   [tool.blank-line-after-blocks]
   exclude = ["tests/", "_generated\.py$", "vendor/", "build/"]
   ```

## Python Coding Style

- Always add type hints where appropriate
- Use "modern" type hints (such as "dict" instead of "typing.Dict")
- Use absolute import instead of relative import
- Code formatted with muff (line length 79, single quotes)
- Strict mypy type checking enabled
- Comprehensive flake8 linting with multiple plugins
