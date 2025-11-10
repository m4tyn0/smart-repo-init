#!/usr/bin/env python3
"""
Unit tests for quick_init_project.py
"""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from quick_init_project import check_coderabbit, load_template, print_install_instructions, run


class TestQuickInitFunctions(unittest.TestCase):
    """Test cases for quick_init_v2.py functions."""

    @patch('subprocess.run')
    def test_run_success(self, mock_run):
        """Test run function with successful command."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'status'],
            returncode=0,
            stdout='On branch main',
            stderr=''
        )

        result = run(['git', 'status'])

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, 'On branch main')
        mock_run.assert_called_once_with(
            ['git', 'status'],
            capture_output=True,
            text=True
        )

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('subprocess.run')
    def test_run_failure_with_check(self, mock_run, mock_exit, mock_print):
        """Test run function with failed command and check=True."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'invalid'],
            returncode=1,
            stdout='',
            stderr='error message'
        )

        run(['git', 'invalid'], check=True)

        # Should print error and exit
        self.assertTrue(mock_print.called)
        mock_exit.assert_called_once_with(1)

    @patch('subprocess.run')
    def test_run_failure_without_check(self, mock_run):
        """Test run function with failed command and check=False."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'invalid'],
            returncode=1,
            stdout='',
            stderr='error message'
        )

        result = run(['git', 'invalid'], check=False)

        # Should not raise or exit, just return the result
        self.assertEqual(result.returncode, 1)

    @patch('subprocess.run')
    def test_check_coderabbit_installed(self, mock_run):
        """Test check_coderabbit when CodeRabbit is installed."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['which', 'coderabbit'],
            returncode=0,
            stdout='/usr/local/bin/coderabbit',
            stderr=''
        )

        result = check_coderabbit()

        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ['which', 'coderabbit'],
            capture_output=True,
            text=True
        )

    @patch('subprocess.run')
    def test_check_coderabbit_not_installed(self, mock_run):
        """Test check_coderabbit when CodeRabbit is not installed."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['which', 'coderabbit'],
            returncode=1,
            stdout='',
            stderr=''
        )

        result = check_coderabbit()

        self.assertFalse(result)

    @patch('builtins.print')
    def test_print_install_instructions(self, mock_print):
        """Test print_install_instructions outputs instructions."""
        print_install_instructions()

        # Check that print was called
        self.assertTrue(mock_print.called)

        # Check for key installation information
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('coderabbit' in str(c).lower() for c in print_calls))
        self.assertTrue(any('install.sh' in str(c).lower() for c in print_calls))

    @patch.object(Path, 'read_text', return_value='template content')
    @patch.object(Path, 'exists', return_value=True)
    def test_load_template_exists(self, mock_exists, mock_read):
        """Test load_template when template file exists."""
        templates_dir = Path('/tmp/templates')
        result = load_template('gitignore.python', templates_dir)

        self.assertEqual(result, 'template content')

    @patch.object(Path, 'exists', return_value=False)
    def test_load_template_not_exists(self, mock_exists):
        """Test load_template when template file doesn't exist."""
        templates_dir = Path('/tmp/templates')
        result = load_template('nonexistent.txt', templates_dir)

        self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()
