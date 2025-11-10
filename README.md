# Smart Repo Init

Quick setup for new repositories with git best practices and CodeRabbit code reviews.

## Quick Start

```bash
# 1. Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login

# 2. Initialize a project
mkdir myproject && cd myproject
python ./scripts/quick_init_project.py
```

## What It Does

- ✅ Initializes git repository with `main` branch
- ✅ Creates `.gitignore`, `.gitattributes`, and `.coderabbit.yaml`
- ✅ Sets up pre-commit hook for automatic code reviews
- ✅ Creates initial commit with all files

## Scripts

### `quick_init_project.py` (Recommended)
Fast setup with sensible defaults:
```bash
python ./scripts/quick_init_project.py
```

### `full_init_project.py` (Advanced)
Full-featured with options:
```bash
python ./scripts/full_init_project.py --path ~/projects/my-app --language python
python ./scripts/full_init_project.py --no-readme --templates-dir ~/.config/templates
```

**Available options:**
- `--path <directory>` - Initialize in specific directory (default: current)
- `--language <lang>` - Use language-specific .gitignore (default: python)
- `--no-readme` - Skip README.md creation
- `--templates-dir <path>` - Use custom templates directory
- `--no-workflow` - Skip workflow explanation

## Templates

All templates are in the `templates/` directory and easily customizable:

- `gitignore.python` - Python-specific ignores
- `gitignore.generic` - Generic ignores
- `gitattributes` - Line ending configuration
- `coderabbit.yaml` - Code review settings
- `pre-commit` - Git hook script

## CodeRabbit Workflow

```
You code → git add → git commit
                        ↓
                Pre-commit hook runs
                        ↓
                CodeRabbit reviews
                        ↓
            ✅ Pass or ❌ Fix issues
```

## Installation (Optional)

Make scripts globally available:

```bash
# Install globally (adds scripts to ~/bin)
./install.sh
source ~/.zshrc  # or ~/.bashrc, ~/.profile

# Now use anywhere
mkdir myproject && cd myproject && project-init
```

**What `./install.sh` does:**
- Copies scripts to `~/bin/` directory
- Makes them executable
- Adds `~/bin` to your PATH (requires shell restart)
- Enables `project-init` command from anywhere

### Uninstall

To remove the installed scripts:

```bash
# Uninstall globally installed scripts
./scripts/uninstall.sh
source ~/.zshrc  # or ~/.bashrc, ~/.profile
```

**What `./scripts/uninstall.sh` does:**
- Removes `~/bin/project-init` and `~/bin/project-init-full`
- Removes `~/bin/templates` directory
- Removes empty `~/bin` directory if no other files exist
- Removes the PATH modification from your shell config

## Customization

### Edit Templates
```bash
vim templates/coderabbit.yaml    # Review settings
vim templates/gitignore.python   # Ignored files
```

### Custom Template Sets
```bash
# Create project-type templates
mkdir ~/.config/templates/web
cp templates/* ~/.config/templates/web/
echo "node_modules/" >> ~/.config/templates/web/gitignore.generic

# Use them
python ./scripts/full_init_project.py --templates-dir ~/.config/templates/web
```

## Testing

The project includes comprehensive unit tests for all core functionality.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
./run_tests.sh

# Or run with pytest directly
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=scripts --cov-report=term-missing
```

### Test Structure

- `tests/test_full_init_project.py` - Tests for ProjectInitializer class
- `tests/test_quick_init_project.py` - Tests for quick_init_project.py functions

All tests use unittest framework with mocking for subprocess calls and file operations.

## Troubleshooting

**CodeRabbit not found:**
```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login
```

**Pre-commit hook not working:**
```bash
chmod +x .git/hooks/pre-commit
```

**Git user not configured:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## License

MIT