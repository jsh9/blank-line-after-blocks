from __future__ import annotations

import re
from pathlib import Path


def should_exclude_file(file_path: Path, exclude_pattern: str) -> bool:
    """Check if a file should be excluded based on the regex pattern."""
    if not exclude_pattern:
        return False

    try:
        pattern = re.compile(exclude_pattern)
        return bool(pattern.search(file_path.as_posix()))
    except re.error:
        # Invalid regex pattern, don't exclude anything
        return False
