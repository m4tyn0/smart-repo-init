# Quick Reference Guide

## 🚀 One-Line Setup

```bash
# Initialize new project
mkdir myproject && cd myproject && python /path/to/quick_init_v2.py
```

## 📦 Install CodeRabbit CLI

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit configure
```

## 🔄 Daily Workflow

```bash
# 1. Make changes
vim myfile.py

# 2. Stage changes
git add myfile.py

# 3. Commit (auto-review runs)
git commit -m "Add feature X"

# If review fails, fix and retry
# Or skip (not recommended):
git commit --no-verify -m "Quick fix"
```

## 🎨 Customize Templates

```bash
# Edit template for future projects
vim templates/coderabbit.yaml
vim templates/gitignore.python
vim templates/pre-commit

# Use custom templates
python init_project_v2.py --templates-dir ~/.config/my-templates
```

## ⚙️ CodeRabbit Config (.coderabbit.yaml)

```yaml
language: en
reviews:
  auto_review: true
  instructions: |
    - Focus on security
    - Check type hints
    - Ensure error handling
```

## 🛠️ Common Commands

```bash
# Initialize with options
python init_project_v2.py --path ~/projects/new-app
python init_project_v2.py --language generic
python init_project_v2.py --no-readme

# Check CodeRabbit status
coderabbit --version
which coderabbit

# Manual review
coderabbit review file.py

# Configure CodeRabbit
coderabbit configure
```

## 🔧 Troubleshooting

```bash
# Fix hook permissions
chmod +x .git/hooks/pre-commit

# Check git config
git config --get user.name
git config --get user.email

# Set git config
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Reinstall CodeRabbit
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

## 📁 File Structure

```
your-project/
├── .git/
│   └── hooks/
│       └── pre-commit       # Auto-review hook
├── .gitignore               # Language-specific
├── .gitattributes           # Line endings
├── .coderabbit.yaml         # Review config
└── README.md                # (optional)
```

## 💡 Pro Tips

### For ADHD-Friendly Workflow
```bash
# Set up once, forget forever
alias new-project='f(){ mkdir "$1" && cd "$1" && project-init; }; f'

# Usage:
new-project my-awesome-app
```

### Skip Review for WIP Commits
```bash
# Only on feature branches!
git commit -n -m "WIP: experimenting"
```

### Batch Setup Multiple Projects
```bash
for name in api web worker; do
  mkdir $name && cd $name && project-init && cd ..
done
```

### Custom Templates Per Project Type
```bash
# Web projects
python init_project_v2.py --templates-dir ~/templates/web

# Data science projects  
python init_project_v2.py --templates-dir ~/templates/datascience

# CLI tools
python init_project_v2.py --templates-dir ~/templates/cli
```

## 📚 Learn More

- **Full Workflow**: See `CODERABBIT_WORKFLOW.md`
- **Template Customization**: Edit files in `templates/`
- **CodeRabbit Docs**: https://www.coderabbit.ai/docs/cli

## 🆘 Quick Help

```bash
# Show help
python init_project_v2.py --help

# Test CodeRabbit
echo "print('hello')" > test.py
git add test.py
coderabbit review test.py
```
