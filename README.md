# blank-line-after-blocks

A Python formatter to automatically add blank lines after if/for/while/with/try
blocks to improve code readability.

## Installation

```bash
pip install blank-line-after-blocks
```

## Usage

### Command Line

```bash
# Format Python files
blank-line-after-blocks file1.py file2.py

# Format Jupyter notebooks
blank-line-after-blocks-jupyter notebook1.ipynb notebook2.ipynb
```

### Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/your-username/blank-line-after-blocks
    rev: v0.1.0
    hooks:
      - id: blank-line-after-blocks
      - id: blank-line-after-blocks-jupyter
```

## What it does

This tool automatically adds one blank line after the end of:

- `if` statements
- `for` loops
- `while` loops
- `with` statements
- `try`/`except`/`finally` blocks

This improves code readability by providing visual separation between blocks
and subsequent code.

## Example

**Before:**

```python
if condition:
    do_something()
next_statement()

for item in items:
    process(item)
final_step()
```

**After:**

```python
if condition:
    do_something()

next_statement()

for item in items:
    process(item)

final_step()
```
