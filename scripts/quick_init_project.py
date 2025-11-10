#!/usr/bin/env python3
"""
Quick Project Init - Fast setup with sensible defaults
Usage: python quick_init.py
"""

from pathlib import Path
import subprocess
import sys
import time


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and optionally exit on failure."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    return result


def check_coderabbit() -> bool:
    """Check if CodeRabbit CLI is installed."""
    result = run(["which", "coderabbit"], check=False)
    return result.returncode == 0


def print_install_instructions() -> None:
    """Print CodeRabbit installation instructions."""
    print("\n" + "="*60)
    print("📦 CodeRabbit CLI Installation")
    print("="*60)
    print("\nRun this command:")
    print("\n  curl -fsSL https://cli.coderabbit.ai/install.sh | sh")
    print("\nThen configure it:")
    print("  coderabbit configure")
    print("\n" + "="*60)


def load_template(template_name: str, templates_dir: Path) -> str:
    """Load a template file."""
    template_path = templates_dir / template_name
    if template_path.exists():
        return template_path.read_text()
    return None


def setup_remote_and_push() -> None:
    """Setup git remote and push to remote repository."""
    print("\n🌐 Setting up remote repository...")

    # Check if remote already exists
    result = run(["git", "remote", "get-url", "origin"], check=False)

    if result.returncode == 0:
        remote_url = result.stdout.strip()
        print(f"✅ Remote 'origin' already exists: {remote_url}")
        push_to_existing = input("   Push to this remote? (y/n): ").lower()
        if push_to_existing != 'y':
            print("   Skipping push to remote.")
            return
    else:
        # No remote exists, ask user if they want to add one
        print("📡 No remote repository configured.")
        add_remote = input("   Add a remote repository? (y/n): ").lower()

        if add_remote != 'y':
            print("   Skipping remote setup. You can add it later with:")
            print("   git remote add origin <url>")
            print("   git push -u origin main")
            return

        # Get remote URL from user
        remote_url = input("   Enter remote repository URL (e.g., git@github.com:user/repo.git): ").strip()

        if not remote_url:
            print("   No URL provided, skipping remote setup.")
            return

        # Add the remote
        print(f"   Adding remote 'origin': {remote_url}")
        result = run(["git", "remote", "add", "origin", remote_url], check=False)
        if result.returncode != 0:
            print("   ❌ Failed to add remote")
            return
        print("   ✅ Remote added successfully")

    # Push to remote with retry logic
    print("\n📤 Pushing to remote...")
    max_retries = 4
    retry_delays = [2, 4, 8, 16]  # Exponential backoff

    for attempt in range(max_retries):
        result = run(["git", "push", "-u", "origin", "main"], check=False)
        if result.returncode == 0:
            print("✅ Successfully pushed to remote!")
            return
        else:
            if attempt < max_retries - 1:
                delay = retry_delays[attempt]
                print(f"   ⚠️  Push failed (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"   ❌ Failed to push after {max_retries} attempts")
                print(f"   Error: {result.stderr}")
                print("\n   You can push manually later with:")
                print("   git push -u origin main")
                return


def main():
    path = Path.cwd()
    
    # Find templates directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    
    # Check if empty
    files = [f for f in path.iterdir() if not f.name.startswith('.')]
    if files:
        print("⚠️  Folder not empty!")
        if input("Continue? (y/n): ").lower() != 'y':
            sys.exit(0)
    
    print("🚀 Initializing project...\n")
    
    # Git init
    if not (path / ".git").exists():
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
        print("✅ Git initialized")
    
    # .gitignore
    gitignore_content = load_template("gitignore.python", templates_dir)
    if gitignore_content:
        (path / ".gitignore").write_text(gitignore_content)
        print("✅ .gitignore created from template")
    else:
        # Fallback minimal version
        (path / ".gitignore").write_text("""
__pycache__/
*.py[cod]
.venv/
venv/
.env
.DS_Store
.idea/
.vscode/
""".strip())
        print("✅ .gitignore created (minimal)")
    
    # .gitattributes
    gitattributes_content = load_template("gitattributes", templates_dir)
    if gitattributes_content:
        (path / ".gitattributes").write_text(gitattributes_content)
        print("✅ .gitattributes created from template")
    else:
        (path / ".gitattributes").write_text("* text=auto eol=lf\n")
        print("✅ .gitattributes created (minimal)")
    
    # CodeRabbit config
    coderabbit_content = load_template("coderabbit.yaml", templates_dir)
    if coderabbit_content:
        (path / ".coderabbit.yaml").write_text(coderabbit_content)
        print("✅ CodeRabbit config created from template")
    else:
        (path / ".coderabbit.yaml").write_text("""
language: en
reviews:
  auto_review: true
  request_changes_workflow: true
""".strip())
        print("✅ CodeRabbit config created (minimal)")
    
    # Check CodeRabbit installation
    coderabbit_installed = check_coderabbit()
    if not coderabbit_installed:
        print("⚠️  CodeRabbit CLI not installed")
    else:
        print("✅ CodeRabbit CLI is installed")
    
    # Pre-commit hook
    hooks_dir = path / ".git" / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    hook = hooks_dir / "pre-commit"
    
    hook_content = load_template("pre-commit", templates_dir)
    if hook_content:
        hook.write_text(hook_content)
        print("✅ Pre-commit hook created from template")
    else:
        # Fallback minimal version
        hook.write_text("""#!/bin/sh
echo "🐰 Running CodeRabbit review..."
if ! command -v coderabbit &> /dev/null; then
    echo "⚠️  CodeRabbit CLI not found!"
    echo "Install: curl -fsSL https://cli.coderabbit.ai/install.sh | sh"
    exit 0
fi
coderabbit review || exit 1
""")
        print("✅ Pre-commit hook created (minimal)")
    
    hook.chmod(0o755)
    
    # Initial commit
    git_user = run(["git", "config", "user.name"], check=False)
    git_email = run(["git", "config", "user.email"], check=False)
    
    if git_user.returncode == 0 and git_email.returncode == 0:
        run(["git", "add", "."])
        run(["git", "commit", "--no-verify", "-m", "Initial commit: Project setup with CodeRabbit CLI"])
        print("✅ Initial commit done (pre-commit hook skipped for setup)")

        # Setup remote and push
        setup_remote_and_push()
    else:
        print("⚠️  Git user not configured - skipping initial commit")
        print("   Set with: git config --global user.name 'Your Name'")
        print("             git config --global user.email 'you@example.com'")

    print("\n🎉 Done!\n")
    
    # Print installation instructions if needed
    if not coderabbit_installed:
        print_install_instructions()
    
    # Print workflow explanation
    print("\n" + "="*60)
    print("🐰 How It Works")
    print("="*60)
    print("""
When you commit:
  1. git commit -m "message"
  2. Pre-commit hook runs automatically
  3. CodeRabbit reviews your changes
  4. If issues found → commit blocked
  5. If all good → commit proceeds

To skip the hook (not recommended):
  git commit --no-verify -m "message"

Next steps:
  • Customize .coderabbit.yaml for your needs
  • Start coding!
""")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
