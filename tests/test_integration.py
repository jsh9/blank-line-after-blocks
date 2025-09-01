"""Integration tests for blank-line-after-blocks formatter."""

import pytest
import tempfile
import os
from blank_line_after_blocks.main_py import main as main_py
from blank_line_after_blocks.helper import fix_src


class TestIntegration:
    """Integration tests that test the full pipeline."""

    @pytest.mark.parametrize(
        'input_code,expected_output,description',
        [
            # Basic if statement
            (
                "if True:\n    print('hello')\nprint('world')",
                "if True:\n    print('hello')\n\nprint('world')",
                'Basic if statement',
            ),
            # Multiple nested blocks
            (
                'def function():\n    if condition:\n        for item in items:\n            process(item)\n        done_processing()\n    final_step()',
                'def function():\n    if condition:\n        for item in items:\n            process(item)\n\n        done_processing()\n\n    final_step()',
                'Nested blocks within function',
            ),
            # Complex control flow
            (
                'try:\n    risky_operation()\nexcept ValueError as e:\n    handle_value_error(e)\nexcept Exception as e:\n    handle_general_error(e)\nfinally:\n    cleanup()\nfinal_step()',
                'try:\n    risky_operation()\nexcept ValueError as e:\n    handle_value_error(e)\nexcept Exception as e:\n    handle_general_error(e)\nfinally:\n    cleanup()\n\nfinal_step()',
                'Try-except-finally block',
            ),
            # With statement
            (
                "with open('file.txt') as f:\n    content = f.read()\nprocess_content(content)",
                "with open('file.txt') as f:\n    content = f.read()\n\nprocess_content(content)",
                'With statement',
            ),
            # Already formatted code (no changes needed)
            (
                'if condition:\n    do_something()\n\nnext_statement()',
                'if condition:\n    do_something()\n\nnext_statement()',
                'Already formatted code',
            ),
            # Code without blocks (no changes needed)
            (
                'x = 5\ny = 10\nresult = x + y\nprint(result)',
                'x = 5\ny = 10\nresult = x + y\nprint(result)',
                'Code without blocks',
            ),
            # Function definitions (should not add blank lines after def)
            (
                'def my_function():\n    return 42\nother_code()',
                'def my_function():\n    return 42\nother_code()',
                'Function definition',
            ),
            # Class definitions (should not add blank lines after class)
            (
                'class MyClass:\n    def method(self):\n        pass\nother_code()',
                'class MyClass:\n    def method(self):\n        pass\nother_code()',
                'Class definition',
            ),
            # While loop with else
            (
                'while condition:\n    do_work()\nelse:\n    no_break_occurred()\nafter_while()',
                'while condition:\n    do_work()\n\nelse:\n    no_break_occurred()\n\nafter_while()',
                'While loop with else clause',
            ),
            # For loop with else
            (
                'for item in items:\n    if process(item):\n        break\nelse:\n    all_processed()\nafter_for()',
                'for item in items:\n    if process(item):\n        break\n\nelse:\n    all_processed()\n\nafter_for()',
                'For loop with else clause',
            ),
        ],
    )
    def test_fix_src_integration(
            self, input_code, expected_output, description
    ):
        """Test fix_src function with various real-world scenarios."""
        result = fix_src(input_code)
        assert result == expected_output, f'Failed for: {description}'

    def test_end_to_end_file_processing(self):
        """Test the complete file processing pipeline."""
        input_code = """# Test Python file
def main():
    items = [1, 2, 3, 4, 5]

    for item in items:
        if item % 2 == 0:
            print(f"Even: {item}")
        else:
            print(f"Odd: {item}")
    print("Processing complete")

    try:
        with open("data.txt") as f:
            data = f.read()
        process_data(data)
    except FileNotFoundError:
        print("File not found")
    print("All done")

if __name__ == "__main__":
    main()
"""

        expected_output = """# Test Python file
def main():
    items = [1, 2, 3, 4, 5]

    for item in items:
        if item % 2 == 0:
            print(f"Even: {item}")
        else:
            print(f"Odd: {item}")

    print("Processing complete")

    try:
        with open("data.txt") as f:
            data = f.read()

        process_data(data)
    except FileNotFoundError:
        print("File not found")

    print("All done")

if __name__ == "__main__":
    main()
"""

        # Test the fix_src function directly
        result = fix_src(input_code)
        assert result == expected_output

        # Test through the main function
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(input_code)
            temp_filename = f.name

        try:
            # Run the formatter on the file
            try:
                main_py([temp_filename])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            assert exit_code == 1  # Changes were made

            # Verify the file was modified correctly
            with open(temp_filename) as f:
                modified_content = f.read()

            assert modified_content == expected_output

        finally:
            os.unlink(temp_filename)

    def test_no_changes_needed(self):
        """Test that files needing no changes are not modified."""
        input_code = """# Already well formatted
def function():
    return "hello world"

x = 1
y = 2
result = x + y
print(result)
"""

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(input_code)
            temp_filename = f.name

        try:
            # Run the formatter
            try:
                main_py([temp_filename])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            assert exit_code == 0  # No changes were made

            # Verify the file was not modified
            with open(temp_filename) as f:
                content = f.read()

            assert content == input_code

        finally:
            os.unlink(temp_filename)

    @pytest.mark.integration
    def test_directory_processing(self):
        """Test processing multiple files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            files_data = {
                'file1.py': "if True:\n    print('file1')\nprint('done')",
                'file2.py': "for i in range(3):\n    print(i)\nprint('finished')",
                'file3.py': "# No blocks\nprint('simple')",
                'not_python.txt': 'This should be ignored',
            }

            expected_results = {
                'file1.py': "if True:\n    print('file1')\n\nprint('done')",
                'file2.py': "for i in range(3):\n    print(i)\n\nprint('finished')",
                'file3.py': "# No blocks\nprint('simple')",
            }

            # Create the files
            for filename, content in files_data.items():
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)

            # Process the directory
            try:
                main_py([temp_dir])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            assert exit_code == 1  # Changes were made

            # Verify results
            for filename, expected_content in expected_results.items():
                filepath = os.path.join(temp_dir, filename)
                with open(filepath) as f:
                    actual_content = f.read()

                assert actual_content == expected_content, (
                    f'File {filename} not processed correctly'
                )

            # Verify non-Python file was not touched
            txt_filepath = os.path.join(temp_dir, 'not_python.txt')
            with open(txt_filepath) as f:
                txt_content = f.read()

            assert txt_content == 'This should be ignored'

    def test_syntax_error_handling(self):
        """Test that files with syntax errors are handled gracefully."""
        invalid_python = (
            'if condition\n    # missing colon\n    do_something()'
        )

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(invalid_python)
            temp_filename = f.name

        try:
            # Should not crash, should return 0 (no changes made)
            try:
                main_py([temp_filename])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            assert exit_code == 0

            # File should be unchanged
            with open(temp_filename) as f:
                content = f.read()

            assert content == invalid_python

        finally:
            os.unlink(temp_filename)
