"""Tests for main_jupyter.py module."""

import pytest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock
from blank_line_after_blocks.main_jupyter import JupyterNotebookFixer, main


class TestJupyterNotebookFixer:
    """Test the JupyterNotebookFixer class."""

    @pytest.fixture
    def sample_notebook(self):
        """Create a sample Jupyter notebook structure."""
        return {
            'cells': [
                {
                    'cell_type': 'code',
                    'source': [
                        'if condition:\n',
                        '    do_something()\n',
                        'next_line()',
                    ],
                },
                {'cell_type': 'markdown', 'source': ['# This is markdown']},
                {
                    'cell_type': 'code',
                    'source': [
                        'for item in items:\n',
                        '    process(item)\n',
                        'after_loop()',
                    ],
                },
            ],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 4,
        }

    @pytest.fixture
    def fixer(self):
        """Create a JupyterNotebookFixer instance."""
        return JupyterNotebookFixer(path='test.ipynb')

    @patch('blank_line_after_blocks.main_jupyter.JupyterNotebookParser')
    @patch('blank_line_after_blocks.main_jupyter.JupyterNotebookRewriter')
    def test_fix_one_file_with_changes(
            self,
            mock_rewriter_class,
            mock_parser_class,
            fixer,
            sample_notebook,
    ):
        """Test fix_one_file when changes are made to notebook cells."""
        # Setup mocks
        mock_parser = MagicMock()
        mock_rewriter = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_rewriter_class.return_value = mock_rewriter

        # Mock source code container
        mock_source_container = MagicMock()
        mock_source_container.source_without_magic = (
            'if condition:\n    do_something()\nnext_line()'
        )
        mock_source_container.magics = {}

        mock_parser.get_code_cells.return_value = [sample_notebook['cells'][0]]
        mock_parser.get_code_cell_indices.return_value = [0]
        mock_parser.get_code_cell_sources.return_value = [
            mock_source_container
        ]
        mock_parser.notebook_content = sample_notebook

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.ipynb', delete=False
        ) as f:
            json.dump(sample_notebook, f)
            temp_filename = f.name

        try:
            with patch(
                'blank_line_after_blocks.main_jupyter.reconstruct_source',
                return_value='if condition:\n    do_something()\n\nnext_line()',
            ):
                with patch('builtins.open', create=True):
                    with patch('json.dump'):
                        result = fixer.fix_one_file(temp_filename)

                        # Should return 1 (changes were made and
                        # exit_zero_even_if_changed is False)
                        assert result == 1

                        # Should call replace_source_in_code_cell
                        mock_method = mock_rewriter.replace_source_in_code_cell
                        mock_method.assert_called_once()

        finally:
            os.unlink(temp_filename)

    @patch('blank_line_after_blocks.main_jupyter.JupyterNotebookParser')
    def test_fix_one_file_parse_error(self, mock_parser_class, fixer):
        """Test fix_one_file when notebook parsing fails."""
        import tempfile
        import os

        mock_parser_class.side_effect = Exception('Parse error')

        # Create a temporary file so the file existence check passes
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.ipynb', delete=False
        ) as f:
            f.write('{}')  # Write minimal content
            temp_filename = f.name

        try:
            with patch('sys.stderr'):
                result = fixer.fix_one_file(temp_filename)
                assert result == 1
        finally:
            os.unlink(temp_filename)

    @patch('blank_line_after_blocks.main_jupyter.JupyterNotebookParser')
    @patch('blank_line_after_blocks.main_jupyter.JupyterNotebookRewriter')
    def test_fix_one_file_no_changes(
            self, mock_rewriter_class, mock_parser_class, fixer
    ):
        """Test fix_one_file when no changes are needed."""
        # Setup mocks
        mock_parser = MagicMock()
        mock_rewriter = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_rewriter_class.return_value = mock_rewriter

        # Mock source that doesn't need fixing
        mock_source_container = MagicMock()
        mock_source_container.source_without_magic = 'simple_statement()'
        mock_source_container.magics = {}

        mock_parser.get_code_cells.return_value = [{}]
        mock_parser.get_code_cell_indices.return_value = [0]
        mock_parser.get_code_cell_sources.return_value = [
            mock_source_container
        ]

        result = fixer.fix_one_file('test.ipynb')

        # Should return 0 (no changes made)
        assert result == 0

        # Should not call replace_source_in_code_cell
        mock_rewriter.replace_source_in_code_cell.assert_not_called()


class TestJupyterMain:
    """Test the main function for Jupyter notebooks."""

    @pytest.mark.parametrize(
        'argv,expected_paths',
        [
            (
                ['notebook1.ipynb', 'notebook2.ipynb'],
                ['notebook1.ipynb', 'notebook2.ipynb'],
            ),
            ([], []),
        ],
    )
    def test_main_argument_parsing(self, argv, expected_paths):
        """Test that main function parses arguments correctly."""
        with patch(
            'blank_line_after_blocks.main_jupyter.JupyterNotebookFixer'
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
            'blank_line_after_blocks.main_jupyter.JupyterNotebookFixer'
        ) as MockFixer:
            # Mock the fixer to return 1 (changes were made)
            mock_fixer_instance = MockFixer.return_value
            mock_fixer_instance.fix_one_directory_or_one_file.return_value = 1

            with pytest.raises(SystemExit) as exc_info:
                main(['test.ipynb'])

            # Should raise SystemExit with code 1 when changes were made
            assert exc_info.value.code == 1

    def test_main_no_arguments(self):
        """Test main with no arguments."""
        # Click's main() always calls sys.exit, even when no files processed
        with pytest.raises(SystemExit) as exc_info:
            main([])

        # Should exit with 0 when no files are processed (no changes made)
        assert exc_info.value.code == 0
