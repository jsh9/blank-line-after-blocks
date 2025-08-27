from __future__ import annotations
import ast
from typing import Any


def fix_src(source_code: str) -> str:
    """Add blank lines after if/for/while/with/try blocks."""
    try:
        tree = ast.parse(source=source_code)
    except SyntaxError:
        # Ignore syntax errors (e.g., Jupyter cells with ipython magics)
        return source_code

    # Find all block statements that need blank lines after them
    blocks_to_fix = _collect_blocks_to_fix(tree)

    if not blocks_to_fix:
        return source_code

    # Split source into lines and add blank lines
    lines = source_code.splitlines(keepends=True)
    return _add_blank_lines(lines, blocks_to_fix)


def _collect_blocks_to_fix(tree: ast.Module) -> set[int]:
    """Collect line numbers where blank lines should be added after blocks."""
    blocks_to_fix = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            # For most blocks, add a blank line after the entire construct
            # But for compound statements, we need special handling

            if (
                isinstance(node, (ast.For, ast.While))
                and hasattr(node, 'orelse')
                and node.orelse
            ):
                # For for-else and while-else, add blank line after main
                # body AND after else
                if node.body:
                    body_end = _get_last_line_of_statements(node.body)
                    if body_end is not None:
                        blocks_to_fix.add(body_end)

                orelse_end = _get_last_line_of_statements(node.orelse)
                if orelse_end is not None:
                    blocks_to_fix.add(orelse_end)
            else:
                # For other blocks (if, with, try, simple for/while), add
                # blank line after entire construct
                end_lineno = _get_block_end_line(node)
                if end_lineno is not None:
                    blocks_to_fix.add(end_lineno)

    return blocks_to_fix


def _get_last_line_of_statements(statements: list[Any]) -> int | None:
    """Get the last line number of a list of statements."""
    if not statements:
        return None

    last_stmt = statements[-1]
    if hasattr(last_stmt, 'end_lineno') and last_stmt.end_lineno is not None:
        return int(last_stmt.end_lineno)

    # Fallback for older Python versions
    if hasattr(last_stmt, 'lineno'):
        return int(last_stmt.lineno)

    return None


def _get_block_end_line(node: Any) -> int:
    """Get the last line number of a block statement."""
    if hasattr(node, 'end_lineno') and node.end_lineno is not None:
        return int(node.end_lineno)

    # Fallback for older Python versions - find the maximum line number
    # in the node's body and orelse/finalbody if they exist
    max_lineno = getattr(node, 'lineno', 0)

    for child in ast.walk(node):
        if hasattr(child, 'lineno') and child.lineno:
            max_lineno = max(max_lineno, child.lineno)

    return max_lineno


def _add_blank_lines(lines: list[str], blocks_to_fix: set[int]) -> str:
    """Add blank lines after specified line numbers."""
    result = []
    i = 0

    while i < len(lines):
        result.append(lines[i])

        # Check if this line number needs a blank line after it
        current_line_num = i + 1
        if current_line_num in blocks_to_fix:
            # Check if next line exists and is not already blank
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(('#', '"""', "'''")):
                    # Add blank line if next line is not empty or a comment/docstring
                    result.append('\n')

        i += 1

    return ''.join(result)
