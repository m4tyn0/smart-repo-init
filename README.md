# Project Initializer

Quick setup for new projects with git best practices and CodeRabbit code reviews.

## Quick Start

```bash
# 1. Install CodeRabbit CLI
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit auth login

# 2. Initialize a project
mkdir myproject && cd myproject
python ./scripts/quick_init_v2.py
```

## What It Does

- ✅ Initializes git repository with `main` branch
- ✅ Creates `.gitignore`, `.gitattributes`, and `.coderabbit.yaml`
- ✅ Sets up pre-commit hook for automatic code reviews
- ✅ Creates initial commit with all files

## Scripts

### `quick_init_v2.py` (Recommended)
Fast setup with sensible defaults:
```bash
python ./scripts/quick_init_v2.py
```

### `init_project_v2.py` (Advanced)
Full-featured with options:
```bash
python ./scripts/init_project_v2.py --path ~/projects/my-app --language python
python ./scripts/init_project_v2.py --no-readme --templates-dir ~/.config/templates
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
python ./scripts/init_project_v2.py --templates-dir ~/.config/templates/web
```

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