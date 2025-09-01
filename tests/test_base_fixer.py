"""Tests for base_fixer.py module."""

import pytest
import tempfile
import os
from pathlib import Path
from blank_line_after_blocks.base_fixer import BaseFixer


class ConcreteFixer(BaseFixer):
    """Concrete implementation of BaseFixer for testing."""

    def __init__(
            self, path: str, return_value: int = 0, exclude_pattern: str = ''
    ):
        super().__init__(path, exclude_pattern=exclude_pattern)
        self.return_value = return_value
        self.processed_files = []

    def fix_one_file(self, filename):
        """Mock implementation that tracks processed files."""
        self.processed_files.append(filename)
        return self.return_value


class TestBaseFixer:
    """Test the BaseFixer base class."""

    def test_init(self):
        """Test BaseFixer initialization."""
        fixer = ConcreteFixer(path='test.py', return_value=0)
        assert fixer.path == 'test.py'

    def test_fix_one_directory_or_one_file_single_file(self):
        """Test fixing a single file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as f:
            f.write('# test content')
            temp_filename = f.name

        try:
            fixer = ConcreteFixer(path=temp_filename, return_value=0)
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 1
            assert Path(fixer.processed_files[0]) == Path(temp_filename)

        finally:
            os.unlink(temp_filename)

    def test_fix_one_directory_or_one_file_directory(self):
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

            fixer = ConcreteFixer(path=temp_dir, return_value=0)
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
            self, return_values, expected_result
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
                def __init__(self, path, return_values):
                    super().__init__(path)
                    self.return_values = return_values
                    self.call_count = 0

                def fix_one_file(self, filename):
                    self.call_count += 1
                    return self.return_values[self.call_count - 1]

            fixer = MultiReturnFixer(
                path=temp_dir, return_values=return_values
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == expected_result

    def test_fix_one_file_not_implemented(self):
        """Test that BaseFixer.fix_one_file raises NotImplementedError."""
        fixer = BaseFixer(path='test.py')

        with pytest.raises(
            NotImplementedError, match='Please implement this method'
        ):
            fixer.fix_one_file('test.py')

    def test_fix_one_directory_or_one_file_nonexistent_path(self):
        """Test behavior with non-existent path."""
        fixer = ConcreteFixer(path='/nonexistent/path')

        # This should not raise an exception, but behavior depends on
        # Path.is_file(). For non-existent paths, it will be treated as a
        # directory
        result = fixer.fix_one_directory_or_one_file()

        # Should return 0 since no .py files found in non-existent directory
        assert result == 0
        assert len(fixer.processed_files) == 0

    def test_fix_one_directory_or_one_file_empty_directory(self):
        """Test processing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            fixer = ConcreteFixer(path=temp_dir)
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 0

    def test_fix_one_directory_or_one_file_directory_no_python_files(self):
        """Test directory with no Python files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create non-Python files
            txt_file = os.path.join(temp_dir, 'test.txt')
            js_file = os.path.join(temp_dir, 'test.js')

            with open(txt_file, 'w') as f:
                f.write('not python')

            with open(js_file, 'w') as f:
                f.write('also not python')

            fixer = ConcreteFixer(path=temp_dir)
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            assert len(fixer.processed_files) == 0

    def test_exclude_functionality_with_regex_pattern(self):
        """Test exclude functionality with regex pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            py_file1 = os.path.join(temp_dir, 'test_included.py')
            py_file2 = os.path.join(temp_dir, 'test_excluded.py')

            # Create subdirectory with Python file (should be excluded
            # by pattern)
            sub_dir = os.path.join(temp_dir, 'subdir')
            os.makedirs(sub_dir)
            py_file3 = os.path.join(sub_dir, 'test.py')

            for py_file in [py_file1, py_file2, py_file3]:
                with open(py_file, 'w') as f:
                    f.write('# test content')

            # Use regex pattern to exclude files with 'excluded' in
            # name and 'subdir' directories
            exclude_pattern = r'excluded|subdir'
            fixer = ConcreteFixer(
                path=temp_dir, return_value=0, exclude_pattern=exclude_pattern
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            # Only the included file should be processed
            assert len(fixer.processed_files) == 1
            processed_path = Path(fixer.processed_files[0])
            assert processed_path.name == 'test_included.py'

    def test_exclude_functionality_with_specific_patterns(self):
        """Test exclude functionality with various regex patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            py_file1 = os.path.join(temp_dir, 'test_included.py')
            py_file2 = os.path.join(temp_dir, 'test_cli_excluded.py')

            for py_file in [py_file1, py_file2]:
                with open(py_file, 'w') as f:
                    f.write('# test content')

            # Use regex pattern to exclude files with 'cli_excluded' in name
            exclude_pattern = r'cli_excluded'
            fixer = ConcreteFixer(
                path=temp_dir, return_value=0, exclude_pattern=exclude_pattern
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            # Only the included file should be processed
            assert len(fixer.processed_files) == 1
            processed_path = Path(fixer.processed_files[0])
            assert processed_path.name == 'test_included.py'

    def test_exclude_patterns_empty(self):
        """Test that empty exclude patterns work correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            py_file1 = os.path.join(temp_dir, 'test1.py')
            py_file2 = os.path.join(temp_dir, 'test2.py')

            for py_file in [py_file1, py_file2]:
                with open(py_file, 'w') as f:
                    f.write('# test content')

            # Empty exclude pattern should process all files
            fixer = ConcreteFixer(
                path=temp_dir, return_value=0, exclude_pattern=''
            )
            result = fixer.fix_one_directory_or_one_file()

            assert result == 0
            # Both files should be processed since exclude is empty
            assert len(fixer.processed_files) == 2
