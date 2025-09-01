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

# Format with exclude patterns (regex - use | for multiple patterns)
blank-line-after-blocks --exclude "tests/|_generated\.py$" src/

# Format Jupyter notebooks
blank-line-after-blocks-jupyter notebook1.ipynb notebook2.ipynb

# Format notebooks with exclude patterns (regex)
blank-line-after-blocks-jupyter --exclude "notebooks/generated/" notebooks/
```

### Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/jsh9/blank-line-after-blocks
    rev: <LATEST_TAG>
    hooks:
      - id: blank-line-after-blocks
      - id: blank-line-after-blocks-jupyter
```

#### Pre-commit with exclude patterns

```yaml
repos:
  - repo: https://github.com/jsh9/blank-line-after-blocks
    rev: <LATEST_TAG>
    hooks:
      - id: blank-line-after-blocks
        args: ["--exclude", "tests/|_generated\.py$"]
      - id: blank-line-after-blocks-jupyter
        args: ["--exclude", "notebooks/generated/"]
```

### Configuration File

You can also configure exclude patterns in `pyproject.toml`:

```toml
[tool.blank-line-after-blocks]
exclude = [
    "tests/",            # Exclude all files in tests directory
    "_generated\.py$",   # Exclude files ending with _generated.py
    "vendor/",           # Exclude all files in vendor directory
    "build/",            # Exclude build directory
]
```

**Note**: CLI `--exclude` options take precedence over configuration file
settings.

## What it does

This tool automatically adds one blank line after the end of:

- `if` statements
- `for` loops
- `while` loops
- `with` statements
- `try`/`except`/`finally` blocks

This improves code readability by providing visual separation between blocks
and subsequent code.

## Examples

### Basic if and for blocks

```diff
  if condition:
      do_something()
+
  next_statement()

  for item in items:
      process(item)
+
  final_step()
```

### Try/except blocks with context managers

```diff
  def process_files(filenames):
      results = []
      for filename in filenames:
          try:
              with open(filename) as f:
                  data = json.load(f)
+
              results.append(data)
          except FileNotFoundError:
              print(f'File {filename} not found')
          except json.JSONDecodeError:
              print(f'Invalid JSON in {filename}')
+
      return results
```

### Nested blocks in class methods

```diff
  class TestClass:
      def method(self):
          try:
              if self.condition():
                  with self.get_context():
                      self.do_work()
+
                  self.cleanup()
+
          except Exception as e:
              self.handle_error(e)
+
          print('method complete')
```
