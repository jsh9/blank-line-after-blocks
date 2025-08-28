from __future__ import annotations
import ast


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
    block_types = (ast.If, ast.For, ast.While, ast.With, ast.Try)

    for node in ast.walk(tree):
        if isinstance(node, block_types):
            # Handle compound statements (for-else, while-else) specially
            if (
                isinstance(node, (ast.For, ast.While))
                and hasattr(node, 'orelse')
                and node.orelse
            ):
                # Add blank line after main body
                if (
                    node.body
                    and hasattr(node.body[-1], 'end_lineno')
                    and node.body[-1].end_lineno is not None
                ):
                    blocks_to_fix.add(node.body[-1].end_lineno)
                # Add blank line after else clause
                if (
                    hasattr(node.orelse[-1], 'end_lineno')
                    and node.orelse[-1].end_lineno is not None
                ):
                    blocks_to_fix.add(node.orelse[-1].end_lineno)
            else:
                # For other blocks, add blank line after entire construct
                if hasattr(node, 'end_lineno') and node.end_lineno is not None:
                    blocks_to_fix.add(node.end_lineno)

    return blocks_to_fix


def _add_blank_lines(lines: list[str], blocks_to_fix: set[int]) -> str:
    """Add blank lines after specified line numbers."""
    result = []

    for i, line in enumerate(lines):
        result.append(line)
        current_line_num = i + 1

        if current_line_num in blocks_to_fix:
            # Check if next line exists and is not already blank
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(('#', '"""', "'''")):
                    result.append('\n')

    return ''.join(result)
