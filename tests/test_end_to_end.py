"""End-to-end tests using real before/after file pairs."""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from blank_line_after_blocks.main_py import main as main_py
from blank_line_after_blocks.main_jupyter import main as main_jupyter


class TestEndToEnd:
    """End-to-end tests that run the formatter on real files."""

    def _get_main_function(self, filename):
        """Get the appropriate main function based on file extension."""
        return main_jupyter if filename.endswith('.ipynb') else main_py

    @pytest.fixture
    def test_data_dir(self):
        """Get the path to test data directory."""
        return Path(__file__).parent / 'test_data'

    @pytest.fixture
    def before_files(self, test_data_dir):
        """Get all before files."""
        before_dir = test_data_dir / 'before'
        py_files = list(before_dir.glob('*.py'))
        ipynb_files = list(before_dir.glob('*.ipynb'))
        return py_files + ipynb_files

    @pytest.fixture
    def get_expected_content(self, test_data_dir):
        """Helper function to get expected content for a file."""

        def _get_expected(filename):
            after_file = test_data_dir / 'after' / filename
            if not after_file.exists():
                raise FileNotFoundError(
                    f'Expected file not found: {after_file}'
                )

            return after_file.read_text()

        return _get_expected

    @pytest.mark.parametrize(
        'filename',
        [
            'basic_if.py',
            'loops_and_with.py',
            'complex_nested.py',
            'no_changes_needed.py',
            'already_formatted.py',
            'edge_cases.py',
            'basic_if.ipynb',
            'loops_and_with.ipynb',
            'complex_nested.ipynb',
            'no_changes_needed.ipynb',
            'already_formatted.ipynb',
            'edge_cases.ipynb',
        ],
    )
    def test_formatter_on_file(
            self, test_data_dir, filename, get_expected_content
    ):
        """Test that formatter produces expected output for each test file."""
        before_file = test_data_dir / 'before' / filename
        main_func = self._get_main_function(filename)
        suffix = '.ipynb' if filename.endswith('.ipynb') else '.py'

        # Copy the before file to a temporary location
        with tempfile.NamedTemporaryFile(
            mode='w', suffix=suffix, delete=False
        ) as temp_file:
            temp_file.write(before_file.read_text())
            temp_filename = temp_file.name

        try:
            # Run the formatter on the temporary file
            try:
                main_func([temp_filename])
                exit_code = 0  # No SystemExit means success with no changes
            except SystemExit as e:
                exit_code = e.code

            # Read the formatted content
            with open(temp_filename) as f:
                formatted_content = f.read()

            # Get expected content
            expected_content = get_expected_content(filename)

            # Compare
            assert formatted_content == expected_content, (
                f'Formatting failed for {filename}'
            )

            # Check appropriate exit code
            if formatted_content == before_file.read_text():
                assert exit_code == 0, (
                    f'Expected exit code 0 (no changes) for {filename}'
                )
            else:
                assert exit_code == 1, (
                    f'Expected exit code 1 (changes made) for {filename}'
                )

        finally:
            os.unlink(temp_filename)

    def test_directory_processing_py(self, test_data_dir):
        """Test processing an entire directory of Python files."""
        # Create a temporary directory with copies of all before files
        with tempfile.TemporaryDirectory() as temp_dir:
            before_dir = test_data_dir / 'before'

            # Copy all Python before files to temp directory
            for before_file in before_dir.glob('*.py'):
                temp_file_path = Path(temp_dir) / before_file.name
                shutil.copy2(before_file, temp_file_path)

            # Run formatter on the directory
            try:
                main_py([temp_dir])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            # Check that changes were made (some files should be different)
            assert exit_code == 1, (
                'Expected changes to be made when processing directory'
            )

            # Verify each file matches expected output
            for before_file in before_dir.glob('*.py'):
                temp_file_path = Path(temp_dir) / before_file.name
                expected_file = test_data_dir / 'after' / before_file.name

                with (
                    open(temp_file_path) as temp_f,
                    open(expected_file) as expected_f,
                ):
                    assert temp_f.read() == expected_f.read(), (
                        f'Directory processing failed for {before_file.name}'
                    )

    def test_directory_processing_ipynb(self, test_data_dir):
        """Test processing an entire directory of Jupyter notebook files."""
        # Create a temporary directory with copies of all before files
        with tempfile.TemporaryDirectory() as temp_dir:
            before_dir = test_data_dir / 'before'

            # Copy all Jupyter notebook before files to temp directory
            for before_file in before_dir.glob('*.ipynb'):
                temp_file_path = Path(temp_dir) / before_file.name
                shutil.copy2(before_file, temp_file_path)

            # Run formatter on the directory
            try:
                main_jupyter([temp_dir])
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            # Check that changes were made (some files should be different)
            assert exit_code == 1, (
                'Expected changes to be made when processing directory'
            )

            # Verify each file matches expected output
            for before_file in before_dir.glob('*.ipynb'):
                temp_file_path = Path(temp_dir) / before_file.name
                expected_file = test_data_dir / 'after' / before_file.name

                with (
                    open(temp_file_path) as temp_f,
                    open(expected_file) as expected_f,
                ):
                    assert temp_f.read() == expected_f.read(), (
                        f'Directory processing failed for {before_file.name}'
                    )

    def test_no_changes_files_return_zero(self, test_data_dir):
        """Test that files needing no changes return exit code 0."""
        files_with_no_changes = [
            'no_changes_needed.py',
            'already_formatted.py',
        ]

        for filename in files_with_no_changes:
            before_file = test_data_dir / 'before' / filename

            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.py', delete=False
            ) as temp_file:
                temp_file.write(before_file.read_text())
                temp_filename = temp_file.name

            try:
                try:
                    main_py([temp_filename])
                    exit_code = 0
                except SystemExit as e:
                    exit_code = e.code

                assert exit_code == 0, f'Expected no changes for {filename}'

                # Verify content is unchanged
                with open(temp_filename) as f:
                    content = f.read()

                assert content == before_file.read_text(), (
                    f'Content unexpectedly changed for {filename}'
                )

            finally:
                os.unlink(temp_filename)

    def test_files_requiring_changes_return_one(self, test_data_dir):
        """Test that files requiring changes return exit code 1."""
        files_with_changes = [
            'basic_if.py',
            'loops_and_with.py',
            'complex_nested.py',
            'edge_cases.py',
        ]

        for filename in files_with_changes:
            before_file = test_data_dir / 'before' / filename

            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.py', delete=False
            ) as temp_file:
                temp_file.write(before_file.read_text())
                temp_filename = temp_file.name

            try:
                try:
                    main_py([temp_filename])
                    exit_code = 0
                except SystemExit as e:
                    exit_code = e.code

                assert exit_code == 1, f'Expected changes for {filename}'

                # Verify content actually changed
                with open(temp_filename) as f:
                    content = f.read()

                assert content != before_file.read_text(), (
                    f'Content should have changed for {filename}'
                )

            finally:
                os.unlink(temp_filename)

    def test_exit_zero_flag(self, test_data_dir):
        """Test that there is no --exit-zero-even-if-changed flag anymore."""
        before_file = test_data_dir / 'before' / 'basic_if.py'

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', delete=False
        ) as temp_file:
            temp_file.write(before_file.read_text())
            temp_filename = temp_file.name

        try:
            # Run with non-existent flag should raise SystemExit
            with pytest.raises(SystemExit):
                main_py([temp_filename, '--exit-zero-even-if-changed'])

        finally:
            os.unlink(temp_filename)

    def test_multiple_files(self, test_data_dir):
        """Test processing multiple files at once."""
        filenames = ['basic_if.py', 'loops_and_with.py']
        temp_files = []

        try:
            # Create temporary copies
            for filename in filenames:
                before_file = test_data_dir / 'before' / filename
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.py', delete=False
                ) as temp_file:
                    temp_file.write(before_file.read_text())
                    temp_files.append(temp_file.name)

            # Process all files at once
            try:
                main_py(temp_files)
                exit_code = 0
            except SystemExit as e:
                exit_code = e.code

            assert exit_code == 1, (
                'Expected changes when processing multiple files'
            )

            # Verify each file was formatted correctly
            for i, filename in enumerate(filenames):
                expected_file = test_data_dir / 'after' / filename
                with (
                    open(temp_files[i]) as temp_f,
                    open(expected_file) as expected_f,
                ):
                    assert temp_f.read() == expected_f.read(), (
                        f'Multiple file processing failed for {filename}'
                    )

        finally:
            for temp_file in temp_files:
                os.unlink(temp_file)

    def test_comprehensive_scenarios(self, test_data_dir):
        """Test that all test scenarios work as expected."""
        # This test ensures all our test files are valid and work
        test_pairs = [
            ('basic_if.py', True),  # Should have changes
            ('loops_and_with.py', True),  # Should have changes
            ('complex_nested.py', True),  # Should have changes
            ('no_changes_needed.py', False),  # Should have no changes
            ('already_formatted.py', False),  # Should have no changes
            ('edge_cases.py', True),  # Should have changes
        ]

        for fn, should_change in test_pairs:
            before_file = test_data_dir / 'before' / fn
            after_file = test_data_dir / 'after' / fn

            # Test that the before and after files exist
            assert before_file.exists(), f'Before file missing: {fn}'
            assert after_file.exists(), f'After file missing: {fn}'

            # Test that the change expectation is correct
            before_content = before_file.read_text()
            after_content = after_file.read_text()

            if should_change:
                assert before_content != after_content, (
                    f'Expected changes for {fn} but before/after are identical'
                )
            else:
                assert before_content == after_content, (
                    f'Expected no changes for {fn} but before/after differ'
                )
