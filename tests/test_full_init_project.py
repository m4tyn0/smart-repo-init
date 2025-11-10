#!/usr/bin/env python3
"""
Unit tests for full_init_project.py
"""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, mock_open, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from full_init_project import ProjectInitializer


class TestProjectInitializer(unittest.TestCase):
    """Test cases for ProjectInitializer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_path = Path("/tmp/test_project")
        self.templates_path = Path("/tmp/templates")

    def test_init_with_default_templates(self):
        """Test initialization with default templates directory."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path)
            self.assertEqual(initializer.project_path, self.test_path)
            self.assertIsNotNone(initializer.templates_dir)

    def test_init_with_custom_templates(self):
        """Test initialization with custom templates directory."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)
            self.assertEqual(initializer.templates_dir, self.templates_path)

    @patch('builtins.print')
    @patch.object(Path, 'exists', return_value=False)
    @patch.object(Path, 'mkdir')
    @patch.object(Path, 'write_text')
    def test_create_basic_templates(self, mock_write, mock_mkdir, mock_exists, mock_print):
        """Test creation of basic templates when directory doesn't exist."""
        initializer = ProjectInitializer(self.test_path)

        # Should have created the templates directory
        self.assertTrue(mock_mkdir.called)

        # Should have written basic template files
        self.assertTrue(mock_write.called)
        self.assertGreaterEqual(mock_write.call_count, 3)  # gitignore, gitattributes, coderabbit

    def test_check_empty_folder_empty(self):
        """Test check_empty_folder returns True for empty folder."""
        with patch.object(Path, 'iterdir', return_value=[Path('.git'), Path('.gitignore')]):
            with patch.object(Path, 'exists', return_value=True):
                initializer = ProjectInitializer(self.test_path, self.templates_path)
                result = initializer.check_empty_folder()
                self.assertTrue(result)

    def test_check_empty_folder_not_empty(self):
        """Test check_empty_folder returns False for non-empty folder."""
        with patch.object(Path, 'iterdir', return_value=[Path('file.txt'), Path('.git')]):
            with patch.object(Path, 'exists', return_value=True):
                initializer = ProjectInitializer(self.test_path, self.templates_path)
                result = initializer.check_empty_folder()
                self.assertFalse(result)

    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test run_command with successful command execution."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'status'],
            returncode=0,
            stdout='On branch main',
            stderr=''
        )

        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)
            result = initializer.run_command(['git', 'status'])

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, 'On branch main')
            mock_run.assert_called_once_with(
                ['git', 'status'],
                cwd=self.test_path,
                capture_output=True,
                text=True,
                check=True
            )

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run, mock_print):
        """Test run_command with failed command execution."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=['git', 'invalid'],
            stderr='error message'
        )

        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            with self.assertRaises(subprocess.CalledProcessError):
                initializer.run_command(['git', 'invalid'])

    @patch('subprocess.run')
    def test_check_coderabbit_installed_true(self, mock_run):
        """Test check_coderabbit_installed when CodeRabbit is installed."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['which', 'coderabbit'],
            returncode=0,
            stdout='/usr/local/bin/coderabbit',
            stderr=''
        )

        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)
            result = initializer.check_coderabbit_installed()
            self.assertTrue(result)

    @patch('subprocess.run')
    def test_check_coderabbit_installed_false(self, mock_run):
        """Test check_coderabbit_installed when CodeRabbit is not installed."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['which', 'coderabbit'],
            returncode=1,
            stdout='',
            stderr=''
        )

        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)
            result = initializer.check_coderabbit_installed()
            self.assertFalse(result)

    @patch('builtins.print')
    def test_print_coderabbit_install_instructions(self, mock_print):
        """Test print_coderabbit_install_instructions outputs instructions."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)
            initializer.print_coderabbit_install_instructions()

            # Check that print was called
            self.assertTrue(mock_print.called)

            # Check for key installation information
            print_calls = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any('coderabbit' in str(c).lower() for c in print_calls))

    @patch('builtins.print')
    @patch('subprocess.run')
    def test_init_git_new_repo(self, mock_run, mock_print):
        """Test init_git with a new repository."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'init'],
            returncode=0,
            stdout='',
            stderr=''
        )

        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            # Mock that .git doesn't exist
            git_path = initializer.project_path / ".git"
            with patch.object(Path, 'exists', return_value=False):
                result = initializer.init_git()

                self.assertTrue(result)
                self.assertTrue(mock_run.called)

    @patch('builtins.print')
    @patch.object(Path, 'exists', return_value=True)
    def test_init_git_already_initialized(self, mock_exists, mock_print):
        """Test init_git when git is already initialized."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            # Mock .git directory exists
            with patch.object(Path, '__truediv__', return_value=Path('/tmp/test_project/.git')):
                with patch.object(Path, 'exists', return_value=True):
                    result = initializer.init_git()

                    self.assertFalse(result)

    @patch('builtins.print')
    @patch.object(Path, 'read_text', return_value='template content with {PROJECT_NAME}')
    @patch.object(Path, 'write_text')
    @patch.object(Path, 'exists', return_value=True)
    def test_copy_template_with_vars(self, mock_exists, mock_write, mock_read, mock_print):
        """Test copy_template with variable replacement."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            initializer.copy_template(
                'README.md',
                'README.md',
                replace_vars={'PROJECT_NAME': 'MyProject'}
            )

            # Check that the template was read and written with variable replacement
            self.assertTrue(mock_write.called)
            write_content = mock_write.call_args[0][0]
            self.assertIn('MyProject', write_content)
            self.assertNotIn('{PROJECT_NAME}', write_content)

    @patch('builtins.print')
    @patch.object(Path, 'read_text', return_value='template content')
    @patch.object(Path, 'write_text')
    @patch.object(Path, 'exists', return_value=True)
    def test_copy_template_without_vars(self, mock_exists, mock_write, mock_read, mock_print):
        """Test copy_template without variable replacement."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            initializer.copy_template('gitignore.python', '.gitignore')

            # Check that the template was read and written
            self.assertTrue(mock_write.called)
            write_content = mock_write.call_args[0][0]
            self.assertEqual(write_content, 'template content')

    @patch('builtins.print')
    @patch.object(Path, 'exists', return_value=False)
    def test_copy_template_not_found(self, mock_exists, mock_print):
        """Test copy_template when template file doesn't exist."""
        with patch.object(Path, 'exists', return_value=True):
            initializer = ProjectInitializer(self.test_path, self.templates_path)

            # Mock template not found
            with patch.object(Path, 'exists', side_effect=lambda: False):
                initializer.copy_template('nonexistent.txt', 'output.txt')

                # Should print warning
                self.assertTrue(mock_print.called)

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists', return_value=True)
    def test_create_gitignore_python(self, mock_exists, mock_copy, mock_print):
        """Test create_gitignore for Python."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.create_gitignore('python')

        mock_copy.assert_called_once_with('gitignore.python', '.gitignore')

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists')
    def test_create_gitignore_fallback(self, mock_exists, mock_copy, mock_print):
        """Test create_gitignore fallback to generic."""
        # Template doesn't exist
        mock_exists.return_value = False

        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.create_gitignore('unknown_language')

        # Should call copy_template twice (once for unknown, once for generic fallback)
        self.assertTrue(mock_copy.called)

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists', return_value=True)
    def test_create_git_attributes(self, mock_exists, mock_copy, mock_print):
        """Test create_git_attributes."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.create_git_attributes()

        mock_copy.assert_called_once_with('gitattributes', '.gitattributes')

    @patch('subprocess.run')
    @patch.object(Path, 'exists', return_value=True)
    def test_check_git_config_configured(self, mock_exists, mock_run):
        """Test check_git_config when git is configured."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'config', 'user.name'],
            returncode=0,
            stdout='John Doe',
            stderr=''
        )

        initializer = ProjectInitializer(self.test_path, self.templates_path)
        has_name, has_email = initializer.check_git_config()

        self.assertTrue(has_name)
        self.assertTrue(has_email)

    @patch('subprocess.run')
    @patch.object(Path, 'exists', return_value=True)
    def test_check_git_config_not_configured(self, mock_exists, mock_run):
        """Test check_git_config when git is not configured."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', 'config', 'user.name'],
            returncode=1,
            stdout='',
            stderr=''
        )

        initializer = ProjectInitializer(self.test_path, self.templates_path)
        has_name, has_email = initializer.check_git_config()

        self.assertFalse(has_name)
        self.assertFalse(has_email)

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'chmod')
    @patch.object(Path, 'mkdir')
    @patch.object(Path, 'exists', return_value=True)
    def test_setup_precommit_hook(self, mock_exists, mock_mkdir, mock_chmod, mock_copy, mock_print):
        """Test setup_precommit_hook."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.setup_precommit_hook()

        # Should create hooks directory
        self.assertTrue(mock_mkdir.called)

        # Should copy template
        mock_copy.assert_called_once_with('pre-commit', '.git/hooks/pre-commit')

        # Should make executable
        self.assertTrue(mock_chmod.called)

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'check_coderabbit_installed', return_value=True)
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists', return_value=True)
    def test_setup_coderabbit_cli_installed(self, mock_exists, mock_copy, mock_check, mock_print):
        """Test setup_coderabbit_cli when CodeRabbit is installed."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.setup_coderabbit_cli()

        mock_check.assert_called_once()
        mock_copy.assert_called_once_with('coderabbit.yaml', '.coderabbit.yaml')

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'check_coderabbit_installed', return_value=False)
    @patch.object(ProjectInitializer, 'print_coderabbit_install_instructions')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists', return_value=True)
    def test_setup_coderabbit_cli_not_installed(self, mock_exists, mock_copy, mock_instructions, mock_check, mock_print):
        """Test setup_coderabbit_cli when CodeRabbit is not installed."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.setup_coderabbit_cli()

        mock_check.assert_called_once()
        mock_instructions.assert_called_once()
        mock_copy.assert_called_once()

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'exists', return_value=True)
    def test_create_readme(self, mock_exists, mock_copy, mock_print):
        """Test create_readme."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.create_readme('TestProject')

        mock_copy.assert_called_once_with(
            'README.md',
            'README.md',
            replace_vars={'PROJECT_NAME': 'TestProject'}
        )

    @patch('builtins.print')
    @patch.object(Path, 'exists', return_value=True)
    def test_print_workflow_explanation(self, mock_exists, mock_print):
        """Test print_workflow_explanation."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.print_workflow_explanation()

        # Check that print was called with workflow information
        self.assertTrue(mock_print.called)
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('workflow' in str(c).lower() or 'coderabbit' in str(c).lower() for c in print_calls))

    @patch('builtins.print')
    @patch.object(ProjectInitializer, 'copy_template')
    @patch.object(Path, 'mkdir')
    @patch.object(Path, 'exists', return_value=True)
    def test_setup_llm_provider_rules(self, mock_exists, mock_mkdir, mock_copy, mock_print):
        """Test setup_llm_provider_rules."""
        initializer = ProjectInitializer(self.test_path, self.templates_path)
        initializer.setup_llm_provider_rules('TestProject')

        # Should create .github directory
        self.assertTrue(mock_mkdir.called)

        # Should copy three templates
        self.assertEqual(mock_copy.call_count, 3)

        # Check that all three templates are copied
        calls = [call[0] for call in mock_copy.call_args_list]
        self.assertTrue(any('cursorrules' in str(c) for c in calls))
        self.assertTrue(any('claude' in str(c) for c in calls))
        self.assertTrue(any('copilot-instructions.md' in str(c) for c in calls))


if __name__ == '__main__':
    unittest.main()
