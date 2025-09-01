# This file is inspired by
# https://github.com/asottile/add-trailing-comma/blob/6be6dfc05176bddfc05176bddfc5a9c4bf0fd4941850f0fb41/add_trailing_comma/_main.py

import sys
from pathlib import Path

import click

import blank_line_after_blocks.helper as helper
from blank_line_after_blocks.base_fixer import BaseFixer


class PythonFileFixer(BaseFixer):
    """Fixer for Python source files."""

    def __init__(self, path: str, exclude_pattern: str = '') -> None:
        super().__init__(path=path, exclude_pattern=exclude_pattern)

    def fix_one_file(self, filename: str) -> int:
        """Fix formatting in a single Python file."""
        if filename == '-':
            source_bytes = sys.stdin.buffer.read()
        else:
            file_path = Path(filename)
            if not file_path.is_file():
                msg = f'{filename} is not a file (skipping)'
                print(msg, file=sys.stderr)
                return 0

            with open(filename, 'rb') as fb:
                source_bytes = fb.read()

        try:
            source_text_orig = source_text = source_bytes.decode()
        except UnicodeDecodeError:
            msg = f'{filename} is non-utf-8 (not supported)'
            print(msg, file=sys.stderr)
            return 1

        source_text = helper.fix_src(source_text)

        if filename == '-':
            print(source_text, end='')
        elif source_text != source_text_orig:
            print(f'Rewriting {filename}', file=sys.stderr)
            with open(filename, 'wb') as f:
                f.write(source_text.encode())

        return source_text != source_text_orig


@click.command()
@click.argument('paths', nargs=-1, type=click.Path())
@click.option(
    '--exclude',
    type=str,
    default='',
    help='Regex pattern to exclude files/directories',
)
def main(paths: tuple[str, ...], exclude: str) -> None:
    """Add blank lines after if/for/while/with/try blocks in Python files."""
    ret = 0
    for path in paths:
        fixer = PythonFileFixer(path=path, exclude_pattern=exclude)
        ret |= fixer.fix_one_directory_or_one_file()

    if ret != 0:
        raise SystemExit(ret)


if __name__ == '__main__':
    raise SystemExit(main())
