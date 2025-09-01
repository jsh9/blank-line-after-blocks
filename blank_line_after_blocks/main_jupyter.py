import json
import sys
from pathlib import Path

import click
from jupyter_notebook_parser import JupyterNotebookParser
from jupyter_notebook_parser import JupyterNotebookRewriter
from jupyter_notebook_parser import SourceCodeContainer
from jupyter_notebook_parser import reconstruct_source

import blank_line_after_blocks.helper as helper
from blank_line_after_blocks.base_fixer import BaseFixer


class JupyterNotebookFixer(BaseFixer):
    """Fixer for Jupyter notebook files."""

    def __init__(self, path: str, exclude_pattern: str = '') -> None:
        super().__init__(path=path, exclude_pattern=exclude_pattern)

    def fix_one_directory_or_one_file(self) -> int:
        """Fix formatting in a single file or all Jupyter notebook files in a directory."""
        from pathlib import Path

        path_obj = Path(self.path)

        if path_obj.is_file():
            return self.fix_one_file(path_obj.as_posix())

        # Process .ipynb files instead of .py files for Jupyter notebooks
        filenames = self._get_files_to_process(path_obj, '*.ipynb')
        all_status = set()
        for filename in filenames:
            status = self.fix_one_file(str(filename))
            all_status.add(status)

        return 0 if not all_status or all_status == {0} else 1

    def fix_one_file(self, filename: str) -> int:
        """Fix formatting in a single Jupyter notebook file."""
        file_path = Path(filename)
        if not file_path.is_file():
            msg = f'{filename} is not a file (skipping)'
            print(msg, file=sys.stderr)
            return 0

        try:
            parsed = JupyterNotebookParser(filename)
            rewriter = JupyterNotebookRewriter(parsed_notebook=parsed)
            code_cells = parsed.get_code_cells()
            code_cell_indices = parsed.get_code_cell_indices()
            code_cell_sources = parsed.get_code_cell_sources()
        except Exception as exc:
            print(f'Error reading {filename}: {str(exc)}', file=sys.stderr)
            return 1
        else:
            ret_val = 0
            assert len(code_cells) == len(code_cell_indices)
            assert len(code_cells) == len(code_cell_sources)

            for i in range(len(code_cells)):
                index: int = code_cell_indices[i]
                source: SourceCodeContainer = code_cell_sources[i]
                source_without_magic: str = source.source_without_magic
                magics: dict[str, str] = source.magics
                fixed: str = helper.fix_src(source_code=source_without_magic)

                if fixed != source_without_magic:
                    ret_val = 1
                    fixed_with_magics = reconstruct_source(fixed, magics)
                    rewriter.replace_source_in_code_cell(
                        index=index,
                        new_source=fixed_with_magics,
                    )

            if ret_val == 1:
                print(f'Rewriting {filename}', file=sys.stderr)
                with open(filename, 'w') as fp:
                    json.dump(parsed.notebook_content, fp, indent=1)
                    # Jupyter notebooks (.ipynb) always ends with a new line
                    # but json.dump does not.
                    fp.write('\n')

            return ret_val


@click.command()
@click.argument('paths', nargs=-1, type=click.Path())
@click.option(
    '--exclude',
    type=str,
    default='',
    help='Regex pattern to exclude files/directories',
)
def main(paths: tuple[str, ...], exclude: str) -> None:
    """Add blank lines after if/for/while/with/try blocks in Jupyter notebooks."""
    ret = 0
    for path in paths:
        fixer = JupyterNotebookFixer(path=path, exclude_pattern=exclude)
        ret |= fixer.fix_one_directory_or_one_file()

    if ret != 0:
        raise SystemExit(ret)


if __name__ == '__main__':
    raise SystemExit(main())
