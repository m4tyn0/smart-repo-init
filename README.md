# Project Initializer with CodeRabbit CLI

Quick Python scripts to initialize a new project with git best practices and automatic CodeRabbit CLI code reviews. **Templates are now external files for easy customization!**

## ✨ Features

- 🔧 Git initialization with `main` branch
- 📝 Customizable `.gitignore` templates (Python, generic, or your own)
- 🔀 `.gitattributes` for consistent line endings
- 🐰 CodeRabbit CLI configuration
- 🪝 Pre-commit hook for automatic code review
- 📄 Optional README.md template
- 🎨 **All templates are external files** - easy to customize!

## 📁 Project Structure

```
project-init/
├── init_project_v2.py          # Full-featured script
├── quick_init_v2.py            # Fast setup with defaults
├── README.md                   # This file
├── CODERABBIT_WORKFLOW.md      # Detailed workflow guide
└── templates/                  # ✨ External templates
    ├── gitignore.python        # Python .gitignore
    ├── gitignore.generic       # Generic .gitignore
    ├── gitattributes           # Git attributes
    ├── coderabbit.yaml         # CodeRabbit config
    ├── pre-commit              # Pre-commit hook
    └── README.md               # Project README template
```

## Quick Start

### Option 1: Quick Init (Fast & Simple)

For instant setup with sensible defaults:

```bash
python quick_init_v2.py
```

This will:
- Set up git with everything you need
- Use templates from the `templates/` directory
- Check if CodeRabbit CLI is installed
- Show you exactly what to do next

### Option 2: Full Init (More Control)

```bash
# In current directory
python init_project_v2.py

# In specific directory
python init_project_v2.py --path /path/to/project

# With generic .gitignore (not Python-specific)
python init_project_v2.py --language generic

# Skip README creation
python init_project_v2.py --no-readme

# Use custom templates directory
python init_project_v2.py --templates-dir ~/.config/my-templates
```

## 📦 Installation

### Step 1: Get the Scripts

```bash
# Clone or download to a convenient location
git clone <repo-url> ~/tools/project-init
cd ~/tools/project-init
```

### Step 2: Install CodeRabbit CLI

```bash
# Official installation command
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Configure (interactive)
coderabbit configure

# Verify
coderabbit --version
```

### Step 3: Make Scripts Globally Available (Optional)

**Option A: Add to PATH**

```bash
# Create a bin directory
mkdir -p ~/bin

# Copy the quick init script
cp quick_init_v2.py ~/bin/project-init
chmod +x ~/bin/project-init

# Copy the templates directory
cp -r templates ~/bin/templates

# Add to PATH in your shell config (~/.zshrc or ~/.bashrc)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Now use it anywhere!
cd /path/to/new/project && project-init
```

**Option B: Create an Alias**

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias project-init='python ~/tools/project-init/quick_init_v2.py'
alias project-init-full='python ~/tools/project-init/init_project_v2.py'
```

## 🎨 Customizing Templates

All templates are in the `templates/` directory. Edit them to match your preferences!

### Add a New Language Template

```bash
# Copy an existing template
cp templates/gitignore.python templates/gitignore.rust

# Edit it for Rust
vim templates/gitignore.rust

# Use it
python init_project_v2.py --language rust
```

### Customize the Pre-commit Hook

```bash
# Edit the pre-commit template
vim templates/pre-commit

# Add custom checks, modify behavior, etc.
```

### Create Your Own Template Set

```bash
# Create your custom templates
mkdir ~/.config/my-project-templates
cp -r templates/* ~/.config/my-project-templates/

# Customize them
vim ~/.config/my-project-templates/coderabbit.yaml

# Use them
python init_project_v2.py --templates-dir ~/.config/my-project-templates
```

## What Gets Created

```
your-project/
├── .git/
│   └── hooks/
│       └── pre-commit          # CodeRabbit review hook
├── .gitignore                  # Language-specific ignores
├── .gitattributes              # Line ending configuration
├── .coderabbit.yaml            # CodeRabbit settings
└── README.md                   # Project template (optional)
```

## 🐰 CodeRabbit Workflow

See [CODERABBIT_WORKFLOW.md](CODERABBIT_WORKFLOW.md) for a comprehensive guide!

### Quick Overview

```
You make changes → Stage files → Commit
                                    ↓
                        Pre-commit hook runs
                                    ↓
                        CodeRabbit reviews
                                    ↓
                ┌──────────────────────────────┐
                ↓                              ↓
          ✅ All good                    ❌ Issues found
          Commit proceeds                Commit blocked
                                        Fix & try again
```

### What Gets Reviewed

- **Code Quality**: Style, complexity, duplication
- **Security**: Vulnerabilities, secrets, input validation
- **Best Practices**: Error handling, resource management
- **Performance**: Inefficient algorithms, memory issues

### Example Review Output

```bash
$ git commit -m "Add user authentication"

🐰 Running CodeRabbit CLI review on staged changes...
Reviewing files:
  - src/auth.py

⚠️  Issues found:

src/auth.py:23
  Hardcoded secret key detected
  Recommendation: Use environment variables

✅ Code quality: Good
⚠️  1 security issue

❌ Please fix issues or use --no-verify to skip
```

## Pre-commit Hook

The pre-commit hook will automatically run CodeRabbit review on staged files before each commit.

**Installation Check**: The hook checks if CodeRabbit CLI is installed and shows install instructions if not:

```bash
⚠️  CodeRabbit CLI not found!

Install it with:
  curl -fsSL https://cli.coderabbit.ai/install.sh | sh

Or visit: https://www.coderabbit.ai/docs/cli
```

**To bypass the hook** (not recommended for production code):
```bash
git commit --no-verify -m "Your message"
```

## ⚙️ Configuration

### CodeRabbit Settings

Edit `.coderabbit.yaml` in your project (or the template before initializing):

```yaml
language: en
reviews:
  auto_review: true
  request_changes_workflow: true
  
  # Add custom instructions
  instructions: |
    - Focus on Python best practices
    - Check for security vulnerabilities
    - Ensure proper error handling
```

See [CODERABBIT_WORKFLOW.md](CODERABBIT_WORKFLOW.md#configuration-options) for advanced configuration.

## 🎓 Tips for ADHD-Friendly Usage

Perfect for quick setup without decision paralysis:

```bash
# One command to rule them all
mkdir myproject && cd myproject && project-init

# No decisions needed - just start coding!
# The pre-commit hook handles quality automatically
```

**Benefits:**
- ✅ Consistent setup every time
- ✅ No forgetting important files
- ✅ Automatic code quality checks
- ✅ Templates are easy to tweak once and forget

## 🔧 Troubleshooting

### "CodeRabbit CLI not found"

The script will show you the install command:
```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

Then configure it:
```bash
coderabbit configure
```

### "Templates directory not found"

The script looks for templates in:
1. `./templates/` (next to the script)
2. Current directory's `./templates/`

Make sure you keep the `templates/` folder with the scripts, or use `--templates-dir`.

### Pre-commit hook not running

```bash
# Make sure it's executable
chmod +x .git/hooks/pre-commit

# Check if hooks are disabled
git config --get core.hooksPath
```

### "Folder is not empty"

The script will ask for confirmation. It's safe to run on non-empty folders - it just adds files without deleting anything.

## 🚀 Advanced Usage

### Create Project-Specific Templates

```bash
# Create a template for web projects
mkdir templates-web
cp templates/* templates-web/
echo "node_modules/" >> templates-web/gitignore.generic

# Use it
python init_project_v2.py --templates-dir templates-web --language generic
```

### Batch Initialize Multiple Projects

```bash
# Create a script
for project in api frontend worker; do
    mkdir $project
    cd $project
    python ~/tools/project-init/quick_init_v2.py
    cd ..
done
```

### Version Control Your Templates

```bash
# Keep templates in their own repo
git clone https://github.com/yourusername/project-templates.git ~/.config/project-templates

# Use them for all projects
python init_project_v2.py --templates-dir ~/.config/project-templates
```

## License

MIT
