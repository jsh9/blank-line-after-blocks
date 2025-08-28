"""Tests for helper.py module."""

import pytest
from blank_line_after_blocks.helper import fix_src


@pytest.mark.parametrize(
    'input_code,expected_output',
    [
        # Test if statement
        (
            'if condition:\n    do_something()\nnext_line()',
            'if condition:\n    do_something()\n\nnext_line()',
        ),
        # Test for loop
        (
            'for item in items:\n    process(item)\nafter_loop()',
            'for item in items:\n    process(item)\n\nafter_loop()',
        ),
        # Test while loop
        (
            'while condition:\n    do_work()\nafter_while()',
            'while condition:\n    do_work()\n\nafter_while()',
        ),
        # Test with statement
        (
            "with open('file.txt') as f:\n    content = f.read()\nprocess(content)",
            "with open('file.txt') as f:\n    content = f.read()\n\nprocess(content)",
        ),
        # Test try statement
        (
            'try:\n    risky_operation()\nexcept Exception:\n    handle_error()\nfinal_step()',
            'try:\n    risky_operation()\nexcept Exception:\n    handle_error()\n\nfinal_step()',
        ),
        # Test nested if statements
        (
            'if outer:\n    if inner:\n        nested_action()\n    inner_done()\nouter_done()',
            'if outer:\n    if inner:\n        nested_action()\n\n    inner_done()\n\nouter_done()',
        ),
        # Test already has blank line - should not add another
        (
            'if condition:\n    do_something()\n\nnext_line()',
            'if condition:\n    do_something()\n\nnext_line()',
        ),
        # Test multiple blocks
        (
            'if first:\n    do_first()\nif second:\n    do_second()\nfinal()',
            'if first:\n    do_first()\n\nif second:\n    do_second()\n\nfinal()',
        ),
    ],
)
def test_fix_src_adds_blank_lines(input_code, expected_output):
    """Test that fix_src adds blank lines after blocks correctly."""
    result = fix_src(input_code)
    assert result == expected_output


@pytest.mark.parametrize(
    'input_code',
    [
        # Test code that shouldn't be modified
        'simple_function_call()',
        'x = 5\ny = 10\nz = x + y',
        # Function definition (not a block that needs blank lines)
        'def my_function():\n    return 42\n\nother_function()',
        # Class definition
        'class MyClass:\n    def method(self):\n        pass\n\nother_code()',
    ],
)
def test_fix_src_no_changes_needed(input_code):
    """Test that fix_src doesn't modify code that doesn't need changes."""
    result = fix_src(input_code)
    assert result == input_code


@pytest.mark.parametrize(
    'input_code',
    [
        # Test malformed Python code
        'if condition\n    missing_colon()',
        # Test incomplete blocks
        'if True:',
        # Test syntax errors
        'def function(\n    # incomplete function definition',
    ],
)
def test_fix_src_handles_syntax_errors(input_code):
    """Test that fix_src handles syntax errors gracefully."""
    # Should return original code unchanged when there are syntax errors
    result = fix_src(input_code)
    assert result == input_code


def test_complex_nested_structure():
    """Test complex nested structure with multiple block types."""
    input_code = """if condition:
    for item in items:
        with open(item) as f:
            try:
                data = f.read()
                process(data)
            except IOError:
                log_error()
        cleanup()
    final_for_step()
final_if_step()"""

    expected = """if condition:
    for item in items:
        with open(item) as f:
            try:
                data = f.read()
                process(data)
            except IOError:
                log_error()

        cleanup()

    final_for_step()

final_if_step()"""

    result = fix_src(input_code)
    assert result == expected


def test_blocks_at_end_of_file():
    """Test that blocks at the end of file are handled correctly."""
    input_code = 'if condition:\n    do_something()'
    expected = input_code  # No next line, so no blank line should be added

    result = fix_src(input_code)
    assert result == expected


@pytest.mark.parametrize(
    'input_code,expected_output',
    [
        # Test if-elif-else
        (
            'if condition1:\n    action1()\nelif condition2:\n    action2()\nelse:\n    action3()\nafter_block()',
            'if condition1:\n    action1()\nelif condition2:\n    action2()\nelse:\n    action3()\n\nafter_block()',
        ),
        # Test try-except-finally
        (
            'try:\n    risky()\nexcept ValueError:\n    handle_value_error()\nexcept Exception:\n    handle_general()\nfinally:\n    cleanup()\nafter_try()',
            'try:\n    risky()\nexcept ValueError:\n    handle_value_error()\nexcept Exception:\n    handle_general()\nfinally:\n    cleanup()\n\nafter_try()',
        ),
        # Test for-else
        (
            'for item in items:\n    if found(item):\n        break\nelse:\n    not_found()\nafter_for()',
            'for item in items:\n    if found(item):\n        break\n\nelse:\n    not_found()\n\nafter_for()',
        ),
    ],
)
def test_compound_statements(input_code, expected_output):
    """Test compound statements (if-elif-else, try-except-finally, etc.)."""
    result = fix_src(input_code)
    assert result == expected_output


def test_indented_blocks():
    """Test that indented blocks within functions/classes are handled correctly."""
    input_code = """def my_function():
    if condition:
        do_something()
    next_statement()

    for item in items:
        process(item)
    final_statement()"""

    expected = """def my_function():
    if condition:
        do_something()

    next_statement()

    for item in items:
        process(item)

    final_statement()"""

    result = fix_src(input_code)
    assert result == expected


def test_empty_blocks():
    """Test blocks with only pass statements."""
    input_code = """if condition:
    pass
next_line()

for item in items:
    pass
after_loop()"""

    expected = """if condition:
    pass

next_line()

for item in items:
    pass

after_loop()"""

    result = fix_src(input_code)
    assert result == expected


def test_flake8_clean_block_cases():
    """Test comprehensive cases from flake8-clean-block project using test data files."""
    # Read the before and after files
    import os

    test_dir = os.path.dirname(os.path.abspath(__file__))
    before_file = os.path.join(
        test_dir, 'test_data', 'before', 'flake8_clean_block_cases.py'
    )
    after_file = os.path.join(
        test_dir, 'test_data', 'after', 'flake8_clean_block_cases.py'
    )

    with open(before_file) as f:
        input_code = f.read()

    with open(after_file) as f:
        expected_output = f.read()

    # Apply the fix_src function to the input
    result = fix_src(input_code)

    # Compare the result with expected output
    assert result == expected_output, (
        'Failed to properly format flake8-clean-block test cases'
    )
