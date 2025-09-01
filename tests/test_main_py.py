"""Tests for main_py.py module."""

import pytest
import tempfile
import os
from unittest.mock import patch
from blank_line_after_blocks.main_py import PythonFileFixer, main


class TestPythonFileFixer:
    """Test the PythonFileFixer class."""

    @pytest.fixture
    def fixer(self):
        """Create a PythonFileFixer instance."""
        return PythonFileFixer(path='test.py')

    def test_fix_one_file_with_changes(self, fixer):
        """Test fix_one_file when changes are made to the file."""
        input_code = 'if condition:\n    do_something()\nnext_line()'
        expected_code = 'if condition:\n    do_something()\n\nnext_line()'

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(input_code)
            temp_filename = f.name

        try:
            # Test that changes are made and file is rewritten
            result = fixer.fix_one_file(temp_filename)

            # Should return 1 (changes were made)
            assert result == 1

            # Check that file was modified
            with open(temp_filename) as f:
                modified_content = f.read()

            assert modified_content == expected_code

        finally:
            os.unlink(temp_filename)

    def test_fix_one_file_no_changes(self, fixer):
        """Test fix_one_file when no changes are needed."""
        input_code = 'simple_statement()'

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write(input_code)
            temp_filename = f.name

        try:
            result = fixer.fix_one_file(temp_filename)

            # Should return 0 (no changes made)
            assert result == 0

            # Check that file was not modified
            with open(temp_filename) as f:
                content = f.read()

            assert content == input_code

        finally:
            os.unlink(temp_filename)

    @patch('sys.stdin')
    @patch('builtins.print')
    def test_fix_one_file_stdin(self, mock_print, mock_stdin, fixer):
        """Test fix_one_file reading from stdin."""
        input_code = 'if condition:\n    do_something()\nnext_line()'
        expected_code = 'if condition:\n    do_something()\n\nnext_line()'

        # Mock stdin.buffer.read()
        mock_stdin.buffer.read.return_value = input_code.encode()

        result = fixer.fix_one_file('-')

        # Should return 1 (changes were made)
        assert result == 1

        # Should print the fixed code to stdout
        mock_print.assert_called_once_with(expected_code, end='')

    def test_fix_one_file_non_utf8(self, fixer):
        """Test fix_one_file with non-UTF-8 file."""
        # Create a file with non-UTF-8 content
        with tempfile.NamedTemporaryFile(
            mode='wb', suffix='.py', delete=False
        ) as f:
            f.write(b'\xff\xfe')  # Invalid UTF-8 bytes
            temp_filename = f.name

        try:
            with patch('sys.stderr'):
                result = fixer.fix_one_file(temp_filename)

                # Should return 1 (error)
                assert result == 1

        finally:
            os.unlink(temp_filename)


class TestMainFunction:
    """Test the main function."""

    @pytest.mark.parametrize(
        'argv,expected_paths',
        [
            (['file1.py', 'file2.py'], ['file1.py', 'file2.py']),
            ([], []),
        ],
    )
    def test_main_argument_parsing(self, argv, expected_paths):
        """Test that main function parses arguments correctly."""
        with patch(
            'blank_line_after_blocks.main_py.PythonFileFixer'
        ) as MockFixer:
            # Mock the fixer to return 0 (no changes)
            mock_fixer_instance = MockFixer.return_value
            mock_fixer_instance.fix_one_directory_or_one_file.return_value = 0

            # Click's main() always calls sys.exit, even for successful runs
            with pytest.raises(SystemExit) as exc_info:
                main(argv)

            # Should exit with 0 since no changes were made
            assert exc_info.value.code == 0

            # Check that the correct number of fixers were created
            assert MockFixer.call_count == len(expected_paths)

            # Check that the correct paths were passed to fixers
            for i, expected_path in enumerate(expected_paths):
                args, kwargs = MockFixer.call_args_list[i]
                assert kwargs['path'] == expected_path

    def test_main_returns_error_code(self):
        """Test that main raises SystemExit when changes are made."""
        with patch(
            'blank_line_after_blocks.main_py.PythonFileFixer'
        ) as MockFixer:
            # Mock the fixer to return 1 (changes were made)
            mock_fixer_instance = MockFixer.return_value
            mock_fixer_instance.fix_one_directory_or_one_file.return_value = 1

            with pytest.raises(SystemExit) as exc_info:
                main(['test.py'])

            # Should raise SystemExit with code 1 when changes were made
            assert exc_info.value.code == 1

    def test_main_multiple_files_mixed_results(self):
        """Test main with multiple files where some have changes and some don't."""
        with patch(
            'blank_line_after_blocks.main_py.PythonFileFixer'
        ) as MockFixer:
            # First file has changes (returns 1), second doesn't (returns 0)
            mock_fixer_instance = MockFixer.return_value
            mock_fixer_instance.fix_one_directory_or_one_file.side_effect = [
                1,
                0,
            ]

            with pytest.raises(SystemExit) as exc_info:
                main(['file1.py', 'file2.py'])

            # Should raise SystemExit with code 1 if any file had
            # changes (using bitwise OR)
            assert exc_info.value.code == 1

    def test_main_no_arguments(self):
        """Test main with no file arguments."""
        # Click's main() always calls sys.exit, even when no files processed
        with pytest.raises(SystemExit) as exc_info:
            main([])

        # Should exit with 0 when no files are processed (no changes made)
        assert exc_info.value.code == 0
