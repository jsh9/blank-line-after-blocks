from __future__ import annotations

from typing import Any
from pathlib import Path

from blank_line_after_blocks.config import should_exclude_file


class BaseFixer:
    """Base class for fixing code formatting issues."""

    def __init__(
            self,
            path: str,
            exclude_pattern: str = r'\.git|\.tox|\.pytest_cache',
    ) -> None:
        """Initialize the fixer with a path and optional exclude pattern."""
        self.path = path
        self.exclude_pattern = exclude_pattern

    def _should_exclude(self, file_path: Path) -> bool:
        """Check if a file should be excluded based on exclude pattern."""
        return should_exclude_file(file_path, self.exclude_pattern)

    def _get_files_to_process(
            self, directory: Path, pattern: str
    ) -> list[Path]:
        """Get list of files to process, filtered by exclude pattern."""
        print(f'[DEBUG] Scanning directory: {directory.as_posix()}')
        print(f'[DEBUG] File pattern: {pattern}')
        print(f"[DEBUG] Exclude pattern: '{self.exclude_pattern}'")

        all_files = sorted(directory.rglob(pattern))
        print(
            f"[DEBUG] Found {len(all_files)} files matching pattern '{pattern}':"
        )
        for f in all_files:
            print(f'[DEBUG]   - {f.as_posix()}')

        filtered_files = [f for f in all_files if not self._should_exclude(f)]
        print(
            f'[DEBUG] After exclusion filtering: {len(filtered_files)} files remaining'
        )
        for f in filtered_files:
            print(f'[DEBUG]   + {f.as_posix()}')

        return filtered_files

    def fix_one_directory_or_one_file(self) -> int:
        """Fix formatting in a single file or all Python files in a directory."""
        path_obj = Path(self.path)

        if path_obj.is_file():
            return self.fix_one_file(path_obj.as_posix())

        filenames = self._get_files_to_process(path_obj, '*.py')
        all_status = set()
        for filename in filenames:
            status = self.fix_one_file(filename.as_posix())
            all_status.add(status)

        return 0 if not all_status or all_status == {0} else 1

    def fix_one_file(self, *varargs: Any, **kwargs: Any) -> int:
        """Fix formatting in a single file."""
        raise NotImplementedError('Please implement this method')
