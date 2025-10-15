# 🎯 START HERE

Welcome to your Project Initializer toolkit! This will help you set up new projects quickly and consistently with CodeRabbit code review integration.

## 🚦 First Time Setup (5 minutes)

### Step 1: Install the Tools Globally

```bash
# Navigate to this directory
cd /path/to/project-init

# Run the installer
./install.sh

# Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

✅ Now you can use `project-init` anywhere!

### Step 2: Install CodeRabbit CLI

```bash
# Official install command
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Configure it (interactive)
coderabbit configure

# Verify
coderabbit --version
```

✅ CodeRabbit is ready!

### Step 3: Try It Out

```bash
# Create a test project
mkdir test-project
cd test-project

# Initialize it
project-init

# Check what was created
ls -la
```

✅ You're all set!

## 📖 What to Read Next

1. **First time?** → Read `SUMMARY.md` for overview
2. **Want quick commands?** → See `QUICKREF.md`
3. **Understand CodeRabbit?** → Read `CODERABBIT_WORKFLOW.md`
4. **Need details?** → Check `README.md`

## 🎮 Try These Commands

```bash
# Quick setup (uses all defaults)
mkdir my-api && cd my-api && project-init

# Full setup with options
project-init-full --path ~/projects/my-app --language python

# Use custom templates
project-init-full --templates-dir ~/.config/my-templates
```

## 🐰 How CodeRabbit Works

```
You Code → Stage → Commit
                     ↓
              Pre-commit hook
                     ↓
              CodeRabbit reviews
                     ↓
         Pass ✅ or Fix ❌
```

**Example:**
```bash
$ git commit -m "Add login feature"

🐰 Running CodeRabbit review...
✓ Code quality: Excellent
✓ No security issues
✓ Tests look good
✅ Review passed!
```

## 🎨 Customize Templates

All templates are in `templates/` directory:

```bash
# Edit for your preferences
vim templates/coderabbit.yaml    # Review settings
vim templates/gitignore.python   # Ignored files
vim templates/pre-commit         # Hook behavior

# After editing, new projects will use your templates!
```

## 💡 Quick Tips

**For ADHD-friendly workflow:**
- ✅ One command: `project-init`
- ✅ No decisions needed
- ✅ Automatic quality checks
- ✅ Consistent setup every time

**Common workflow:**
```bash
# Start new project
mkdir cool-project && cd cool-project && project-init

# Code as usual
vim app.py

# Commit (auto-review runs)
git add app.py
git commit -m "Add feature"
```

## 🆘 Quick Troubleshooting

**"CodeRabbit not found"**
```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

**"command not found: project-init"**
```bash
source ~/.zshrc  # or ~/.bashrc
# Or: python quick_init_v2.py
```

**Hook not running?**
```bash
chmod +x .git/hooks/pre-commit
```

## 📚 Documentation Index

- `START_HERE.md` ← You are here!
- `SUMMARY.md` - Overview & getting started
- `README.md` - Complete usage guide  
- `QUICKREF.md` - Command cheat sheet
- `CODERABBIT_WORKFLOW.md` - Workflow deep dive
- `STRUCTURE.txt` - Visual file structure

## 🎯 Next Actions

1. ✅ Run `./install.sh` if not done
2. ✅ Install CodeRabbit CLI
3. ✅ Create test project
4. ✅ Customize templates (optional)
5. 🚀 Build something awesome!

## 🎊 That's It!

You're ready to create projects with:
- ✅ Proper git setup
- ✅ Automatic code review
- ✅ Consistent structure
- ✅ Best practices built-in

**Need help?** Check the docs above or:
- CodeRabbit: https://www.coderabbit.ai/docs/cli
- Git Hooks: https://git-scm.com/docs/githooks

Happy coding! 🎉
