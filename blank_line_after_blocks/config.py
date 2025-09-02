from __future__ import annotations

import re
from pathlib import Path


def should_exclude_file(file_path: Path, exclude_pattern: str) -> bool:
    """Check if a file should be excluded based on the regex pattern."""
    print(f'[DEBUG] Checking exclusion for: {file_path.as_posix()}')
    print(f"[DEBUG] Exclude pattern: '{exclude_pattern}'")

    if not exclude_pattern:
        print(
            f'[DEBUG] No exclude pattern, including file: {file_path.as_posix()}'
        )
        return False

    try:
        exclude_regex = re.compile(exclude_pattern)
        matches = bool(exclude_regex.search(file_path.as_posix()))
        print(
            f'[DEBUG] Pattern match result: {matches} for {file_path.as_posix()}'
        )
        return matches
    except re.error as e:
        # Invalid regex pattern, don't exclude anything
        print(f"[DEBUG] Invalid regex pattern '{exclude_pattern}': {e}")
        return False
