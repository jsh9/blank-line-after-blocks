# blank-line-after-blocks

A Python formatter to automatically add blank lines after if/for/while/with/try
blocks to improve code readability.

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. Installation](#1-installation)
- [2. Usage](#2-usage)
  - [2.1. Command Line](#21-command-line)
  - [2.2. Pre-commit Hook](#22-pre-commit-hook)
    - [2.2.1. Pre-commit with exclude patterns](#221-pre-commit-with-exclude-patterns)
  - [2.3. Configuration File](#23-configuration-file)
- [3. What it does](#3-what-it-does)
- [4. Examples](#4-examples)
  - [4.1. Basic if and for blocks](#41-basic-if-and-for-blocks)
  - [4.2. Try/except blocks with context managers](#42-tryexcept-blocks-with-context-managers)
  - [4.3. Nested blocks in class methods](#43-nested-blocks-in-class-methods)
  - [4.4. Compound blocks stay tight (no blank line before else/elif/except/finally)](#44-compound-blocks-stay-tight-no-blank-line-before-elseelifexceptfinally)

______________________________________________________________________

<!--TOC-->

## 1. Installation

```bash
pip install blank-line-after-blocks
```

## 2. Usage

### 2.1. Command Line

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

### 2.2. Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/jsh9/blank-line-after-blocks
    rev: <LATEST_TAG>
    hooks:
      - id: blank-line-after-blocks
      - id: blank-line-after-blocks-jupyter
```

#### 2.2.1. Pre-commit with exclude patterns

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

### 2.3. Configuration File

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

## 3. What it does

This tool automatically adds one blank line after the end of:

- `if` statements
- `for` loops
- `while` loops
- `with` statements
- `try`/`except`/`finally` blocks

This improves code readability by providing visual separation between blocks
and subsequent code.

## 4. Examples

### 4.1. Basic if and for blocks

```diff
  if condition:
      do_something()
+
  next_statement()

  for item in items:
      process(item)
+
  final_step()

  if a > 3:
      print('a > 3')
      # Already a comment; no new line added
  a += 2
```

### 4.2. Try/except blocks with context managers

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

### 4.3. Nested blocks in class methods

```diff
  class TestClass:
      def method(self):
          try:
              if self.condition():
                  with self.get_context():
                      self.do_work()
+
                  self.cleanup()
          except Exception as e:
              self.handle_error(e)
+
          print('method complete')
```

### 4.4. Compound blocks stay tight (no blank line before else/elif/except/finally)

If a block ends right before the second part of compound blocks (if/else,
try/except, etc.), no blank line is added:

```python
for item in items:
    if found(item):
        break
else:
    not_found()
```
