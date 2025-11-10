# Smart Repo Init

Quick setup for new repositories with git best practices and CodeRabbit code reviews.

## Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **Why uv?** uv is 10-100x faster than pip for installing packages and resolving dependencies.

## Quick Start

```bash
# 1. Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login

# 2. Initialize a project
mkdir myproject && cd myproject
python ./scripts/full_init_project.py
```

## What It Does

- ✅ Initializes git repository with `main` branch
- ✅ Creates `.gitignore`, `.gitattributes`, and `.coderabbit.yaml`
- ✅ Sets up pre-commit hook for automatic code reviews
- ✅ Creates initial commit with all files

## Usage

The script provides flexible options for initializing your project:

```bash
# Basic usage (current directory)
python ./scripts/full_init_project.py

# Specify a directory
python ./scripts/full_init_project.py --path ~/projects/my-app

# Use different language .gitignore
python ./scripts/full_init_project.py --language python

# Custom templates
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

Make the script globally available:

```bash
# Install globally (adds script to ~/bin)
./scripts/install.sh
source ~/.zshrc  # or ~/.bashrc, ~/.profile

# Now use anywhere
mkdir myproject && cd myproject && project-init
```

**What `./scripts/install.sh` does:**
- Copies `full_init_project.py` to `~/bin/project-init`
- Copies templates to `~/bin/templates`
- Makes the script executable
- Adds `~/bin` to your PATH (requires shell restart)
- Enables `project-init` command from anywhere

### Uninstall

To remove the installed script:

```bash
# Uninstall globally installed script
./scripts/uninstall.sh
source ~/.zshrc  # or ~/.bashrc, ~/.profile
```

**What `./scripts/uninstall.sh` does:**
- Removes `~/bin/project-init`
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
mkdir -p ~/.config/templates/web
cp templates/* ~/.config/templates/web/
echo "node_modules/" >> ~/.config/templates/web/gitignore.generic

# Use them
python ./scripts/full_init_project.py --templates-dir ~/.config/templates/web
```

## Testing

The project includes comprehensive unit tests for all core functionality.

### Running Tests

**With uv:**

```bash
# Install dependencies and run tests
./run_tests.sh

# Or manually with uv
uv sync --extra test
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ --cov=scripts --cov-report=term-missing
```

**Without uv:**

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=scripts --cov-report=term-missing
```

> **Note:** The `./run_tests.sh` script automatically detects if `uv` is installed. It falls back to pip if uv is not available.

### Test Structure

- `tests/test_full_init_project.py` - Tests for ProjectInitializer class and all core functionality

All tests use unittest framework with mocking for subprocess calls and file operations.

## Troubleshooting

**uv not found:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your shell or run
source $HOME/.cargo/env
```

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