from __future__ import annotations

import re
from pathlib import Path


def should_exclude_file(file_path: Path, exclude_pattern: str) -> bool:
    """Check if a file should be excluded based on the regex pattern."""
    if not exclude_pattern:
        return False

    try:
        exclude_regex = re.compile(exclude_pattern)
        matches = bool(exclude_regex.search(file_path.as_posix()))
        if matches:
            print(f'[DEBUG] EXCLUDED: {file_path.as_posix()}')
        return matches
    except re.error as e:
        # Invalid regex pattern, don't exclude anything
        print(f"[DEBUG] Invalid regex pattern '{exclude_pattern}': {e}")
        return False
