from __future__ import annotations

import argparse
from typing import Any

from pathlib import Path


class BaseFixer:
    """Base class for fixing code formatting issues."""

    def __init__(self, path: str, cli_args: argparse.Namespace) -> None:
        """Initialize the fixer with a path and CLI arguments."""
        self.path = path
        self.cli_args = cli_args

    def fix_one_directory_or_one_file(self) -> int:
        """Fix formatting in a single file or all Python files in a directory."""
        path_obj = Path(self.path)

        if path_obj.is_file():
            return self.fix_one_file(path_obj.as_posix())

        filenames = sorted(path_obj.rglob('*.py'))
        all_status = set()
        for filename in filenames:
            status = self.fix_one_file(filename.as_posix())
            all_status.add(status)

        return 0 if not all_status or all_status == {0} else 1

    def fix_one_file(self, *varargs: Any, **kwargs: Any) -> int:
        """Fix formatting in a single file."""
        raise NotImplementedError('Please implement this method')
