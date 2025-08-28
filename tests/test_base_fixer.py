"""Tests for base_fixer.py module."""

import argparse
import pytest
import tempfile
import os
from pathlib import Path
from blank_line_after_blocks.base_fixer import BaseFixer


class ConcreteFixer(BaseFixer):
    """Concrete implementation of BaseFixer for testing."""

    def __init__(
            self,
            path: str,
            cli_args: argparse.Namespace,
            return_value: int = 0,
    ):
        super().__init__(path, cli_args)
        self.return_value = return_value
        self.processed_files = []

    def fix_one_file(self, filename):
        """Mock implementation that tracks processed files."""
        self.processed_files.append(filename)
        return self.return_value


class TestBaseFixer:
    """Test the BaseFixer base class."""

    @pytest.fixture
    def mock_args(self):
        """Create mock CLI arguments."""
        return argparse.Namespace()

    def test_init(self, mock_args):
        """Test BaseFixer initialization."""
        fixer = ConcreteFixer(
            path='test.py', cli_args=mock_args, return_value=0
        )
        assert fixer.path == 'test.py'
        assert fixer.cli_args == mock_args

    def test_fix_one_directory_or_one_file_single_file(self, mock_args):
        """Test fixing a single file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write('# test content')
            temp_filename = f.name

        try:
            fixer = ConcreteFixer(
                path=temp_filename, cli_args=mock_args, return_value=0
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 1
            assert Path(fixer.processed_files[0]) == Path(temp_filename)

        finally:
            os.unlink(temp_filename)

    def test_fix_one_directory_or_one_file_directory(self, mock_args):
        """Test fixing all Python files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            py_file1 = os.path.join(temp_dir, 'test1.py')
            py_file2 = os.path.join(temp_dir, 'test2.py')
            txt_file = os.path.join(temp_dir, 'test.txt')  # Should be ignored

            # Create subdirectory with Python file
            sub_dir = os.path.join(temp_dir, 'subdir')
            os.makedirs(sub_dir)
            py_file3 = os.path.join(sub_dir, 'test3.py')

            for py_file in [py_file1, py_file2, py_file3]:
                with open(py_file, 'w') as f:
                    f.write('# test content')

            with open(txt_file, 'w') as f:
                f.write('not a python file')

            fixer = ConcreteFixer(
                path=temp_dir, cli_args=mock_args, return_value=0
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 3

            # Files should be processed in sorted order
            processed_paths = [Path(f).name for f in fixer.processed_files]
            assert 'test1.py' in processed_paths
            assert 'test2.py' in processed_paths
            assert 'test3.py' in processed_paths

    @pytest.mark.parametrize(
        'return_values,expected_result',
        [
            ([0, 0, 0], 0),  # All files successful
            ([1, 0, 0], 1),  # One file failed
            ([0, 1, 1], 1),  # Multiple files failed
            ([1, 1, 1], 1),  # All files failed
        ],
    )
    def test_fix_one_directory_or_one_file_directory_mixed_results(
            self, mock_args, return_values, expected_result
    ):
        """Test directory processing with mixed return values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            py_files = []
            for i, _return_val in enumerate(return_values):
                py_file = os.path.join(temp_dir, f'test{i}.py')
                with open(py_file, 'w') as f:
                    f.write('# test content')

                py_files.append(py_file)

            class MultiReturnFixer(BaseFixer):
                def __init__(self, path, cli_args, return_values):
                    super().__init__(path, cli_args)
                    self.return_values = return_values
                    self.call_count = 0

                def fix_one_file(self, filename):
                    self.call_count += 1
                    return self.return_values[self.call_count - 1]

            fixer = MultiReturnFixer(
                path=temp_dir, cli_args=mock_args, return_values=return_values
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == expected_result

    def test_fix_one_file_not_implemented(self, mock_args):
        """Test that BaseFixer.fix_one_file raises NotImplementedError."""
        fixer = BaseFixer(path='test.py', cli_args=mock_args)

        with pytest.raises(
            NotImplementedError, match='Please implement this method'
        ):
            fixer.fix_one_file('test.py')

    def test_fix_one_directory_or_one_file_nonexistent_path(self, mock_args):
        """Test behavior with non-existent path."""
        fixer = ConcreteFixer(path='/nonexistent/path', cli_args=mock_args)

        # This should not raise an exception, but behavior depends on
        # Path.is_file(). For non-existent paths, it will be treated as a
        # directory
        result = fixer.fix_one_directory_or_one_file()

        # Should return 0 since no .py files found in non-existent directory
        assert result == 0
        assert len(fixer.processed_files) == 0

    def test_fix_one_directory_or_one_file_empty_directory(self, mock_args):
        """Test processing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            fixer = ConcreteFixer(path=temp_dir, cli_args=mock_args)
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 0

    def test_fix_one_directory_or_one_file_directory_no_python_files(
            self, mock_args
    ):
        """Test directory with no Python files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create non-Python files
            txt_file = os.path.join(temp_dir, 'test.txt')
            js_file = os.path.join(temp_dir, 'test.js')

            with open(txt_file, 'w') as f:
                f.write('not python')

            with open(js_file, 'w') as f:
                f.write('also not python')

            fixer = ConcreteFixer(path=temp_dir, cli_args=mock_args)
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 0
