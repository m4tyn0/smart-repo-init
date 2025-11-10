#!/usr/bin/env python3
"""
Project Initialization Script
Initializes a git repository with best practices and CodeRabbit CLI setup.
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


class ProjectInitializer:
    def __init__(self, project_path: Path = Path.cwd(), templates_dir: Optional[Path] = None):
        self.project_path = project_path
        
        # Find templates directory
        if templates_dir is None:
            # Try to find templates relative to script location
            script_dir = Path(__file__).parent
            self.templates_dir = script_dir / "templates"
            
            # Fallback to current directory
            if not self.templates_dir.exists():
                self.templates_dir = Path.cwd() / "templates"
        else:
            self.templates_dir = templates_dir
            
        if not self.templates_dir.exists():
            print(f"⚠️  Templates directory not found: {self.templates_dir}")
            print("Creating basic templates...")
            self._create_basic_templates()
    
    def _create_basic_templates(self) -> None:
        """Create minimal templates if directory doesn't exist."""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create minimal templates
        (self.templates_dir / "gitignore.python").write_text(
            "__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n.DS_Store\n"
        )
        (self.templates_dir / "gitattributes").write_text("* text=auto eol=lf\n")
        (self.templates_dir / "coderabbit.yaml").write_text(
            "language: en\nreviews:\n  auto_review: true\n"
        )
    
    def check_empty_folder(self) -> bool:
        """Check if the folder is empty (except for hidden files)."""
        files = [f for f in self.project_path.iterdir() if not f.name.startswith('.')]
        return len(files) == 0
    
    def run_command(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {' '.join(cmd)}")
            print(f"Error: {e.stderr}")
            raise
    
    def check_coderabbit_installed(self) -> bool:
        """Check if CodeRabbit CLI is installed."""
        result = self.run_command(["which", "coderabbit"], check=False)
        return result.returncode == 0
    
    def print_coderabbit_install_instructions(self) -> None:
        """Print instructions for installing CodeRabbit CLI."""
        print("\n" + "="*60)
        print("📦 CodeRabbit CLI is not installed")
        print("="*60)
        print("\nInstall it with:")
        print("\n  curl -fsSL https://cli.coderabbit.ai/install.sh | sh")
        print("\nOr visit: https://www.coderabbit.ai/docs/cli")
        print("\nAfter installation, restart your terminal and run:")
        print("  coderabbit configure")
        print("="*60 + "\n")
    
    def init_git(self) -> bool:
        """Initialize git repository."""
        print("🔧 Initializing git repository...")
        
        # Check if git is already initialized
        if (self.project_path / ".git").exists():
            print("⚠️  Git already initialized, skipping...")
            return False
        
        self.run_command(["git", "init"])
        self.run_command(["git", "branch", "-M", "main"])
        print("✅ Git initialized with main branch")
        return True
    
    def copy_template(self, template_name: str, destination: str, replace_vars: dict = None) -> None:
        """Copy a template file from templates directory."""
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            print(f"⚠️  Template not found: {template_name}")
            return
        
        content = template_path.read_text()
        
        # Replace variables if provided
        if replace_vars:
            for key, value in replace_vars.items():
                content = content.replace(f"{{{key}}}", value)
        
        dest_path = self.project_path / destination
        dest_path.write_text(content)
        print(f"✅ Created {destination}")
    
    def create_gitignore(self, language: str = "python") -> None:
        """Create .gitignore from template."""
        print(f"📝 Creating .gitignore for {language}...")
        template_name = f"gitignore.{language}"
        
        # Fallback to generic if specific template doesn't exist
        if not (self.templates_dir / template_name).exists():
            print(f"⚠️  Template for {language} not found, using generic...")
            template_name = "gitignore.generic"
        
        self.copy_template(template_name, ".gitignore")
    
    def create_git_attributes(self) -> None:
        """Create .gitattributes from template."""
        print("📝 Creating .gitattributes...")
        self.copy_template("gitattributes", ".gitattributes")
    
    def setup_precommit_hook(self) -> None:
        """Setup pre-commit hook from template."""
        print("🪝 Setting up pre-commit hook...")
        
        hooks_dir = self.project_path / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        self.copy_template("pre-commit", ".git/hooks/pre-commit")
        
        # Make executable
        precommit_path = hooks_dir / "pre-commit"
        precommit_path.chmod(0o755)
        print("✅ Pre-commit hook created and made executable")
    
    def setup_coderabbit_cli(self) -> None:
        """Setup CodeRabbit CLI configuration."""
        print("🐰 Setting up CodeRabbit CLI configuration...")
        
        # Check if coderabbit CLI is installed
        if not self.check_coderabbit_installed():
            self.print_coderabbit_install_instructions()
        else:
            print("✅ CodeRabbit CLI is installed")
        
        # Create configuration
        self.copy_template("coderabbit.yaml", ".coderabbit.yaml")
    
    def create_readme(self, project_name: Optional[str] = None) -> None:
        """Create README.md from template."""
        print("📄 Creating README.md...")
        
        if project_name is None:
            project_name = self.project_path.name
        
        self.copy_template(
            "README.md",
            "README.md",
            replace_vars={"PROJECT_NAME": project_name}
        )
    
    def print_workflow_explanation(self) -> None:
        """Print explanation of the CodeRabbit workflow."""
        print("\n" + "="*60)
        print("🐰 CodeRabbit Workflow Explanation")
        print("="*60)
        print("""
How CodeRabbit Works with Git:

1. 📝 You make code changes
   └─ Edit your files as usual

2. 📦 Stage your changes
   └─ git add .
   
3. 💬 Commit your changes
   └─ git commit -m "Your commit message"
   
4. 🤖 Pre-commit hook triggers automatically
   ├─ CodeRabbit CLI reviews your staged changes
   ├─ Checks for:
   │  • Code quality issues
   │  • Potential bugs
   │  • Security vulnerabilities
   │  • Best practice violations
   │  • Performance issues
   └─ Provides inline suggestions

5. ✅ Two possible outcomes:
   a) Review passes → Commit proceeds ✓
   b) Issues found → Commit blocked ✗
      └─ Review the feedback
      └─ Fix issues and try again
      └─ Or skip with: git commit --no-verify

Benefits:
• Catches issues before they reach your repo
• Learns from your codebase over time
• Provides context-aware suggestions
• Works offline (local analysis)
• Integrates with GitHub/GitLab for PR reviews

Configuration:
• Edit .coderabbit.yaml to customize behavior
• Add path-specific instructions
• Enable/disable specific checks
""")
        print("="*60 + "\n")
    
    def check_git_config(self) -> tuple[bool, bool]:
        """Check if git user name and email are configured."""
        user_name = self.run_command(["git", "config", "user.name"], check=False)
        user_email = self.run_command(["git", "config", "user.email"], check=False)

        return (user_name.returncode == 0, user_email.returncode == 0)

    def setup_remote_and_push(self) -> None:
        """Setup git remote and push to remote repository."""
        print("\n🌐 Setting up remote repository...")

        # Check if remote already exists
        result = self.run_command(["git", "remote", "get-url", "origin"], check=False)

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
            try:
                self.run_command(["git", "remote", "add", "origin", remote_url])
                print("   ✅ Remote added successfully")
            except subprocess.CalledProcessError:
                print("   ❌ Failed to add remote")
                return

        # Push to remote with retry logic
        print("\n📤 Pushing to remote...")
        max_retries = 4
        retry_delays = [2, 4, 8, 16]  # Exponential backoff

        for attempt in range(max_retries):
            try:
                self.run_command(["git", "push", "-u", "origin", "main"])
                print("✅ Successfully pushed to remote!")
                return
            except subprocess.CalledProcessError as e:
                if attempt < max_retries - 1:
                    delay = retry_delays[attempt]
                    print(f"   ⚠️  Push failed (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"   ❌ Failed to push after {max_retries} attempts")
                    print(f"   Error: {e.stderr}")
                    print("\n   You can push manually later with:")
                    print("   git push -u origin main")
                    return
    
    def run(self, language: str = "python", create_readme: bool = True, explain_workflow: bool = True) -> None:
        """Run the full initialization process."""
        print(f"🚀 Initializing project in: {self.project_path}")
        print(f"📁 Templates directory: {self.templates_dir}\n")
        
        # Check if folder is empty
        if not self.check_empty_folder():
            proceed = input("⚠️  Folder is not empty. Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                print("Aborting...")
                sys.exit(0)
        
        # Initialize git
        git_initialized = self.init_git()
        
        # Create git files
        self.create_gitignore(language)
        self.create_git_attributes()
        
        # Setup CodeRabbit
        self.setup_coderabbit_cli()
        
        # Setup pre-commit hook
        if git_initialized:
            self.setup_precommit_hook()
        
        # Create README
        if create_readme:
            self.create_readme()
        
        # Initial commit
        if git_initialized:
            has_name, has_email = self.check_git_config()
            
            if not has_name or not has_email:
                print("\n⚠️  Git user not configured. Skipping initial commit.")
                print("\n📝 Configure with:")
                print("  git config --global user.name 'Your Name'")
                print("  git config --global user.email 'you@example.com'")
            else:
                print("\n📦 Creating initial commit...")
                print("   (Skipping pre-commit hook for initial setup)")
                self.run_command(["git", "add", "."])
                self.run_command(["git", "commit", "--no-verify", "-m", "Initial commit: Project setup with CodeRabbit CLI"])
                print("✅ Initial commit created (pre-commit hook skipped for setup)")

                # Setup remote and push
                self.setup_remote_and_push()

        print("\n🎉 Project initialization complete!")
        
        # Print workflow explanation
        if explain_workflow:
            self.print_workflow_explanation()
        
        # Print next steps
        print("📋 Next steps:")
        if not self.check_coderabbit_installed():
            print("  1. Install CodeRabbit CLI (see instructions above)")
            print("  2. Run: coderabbit configure")
            print("  3. Start coding!")
        else:
            print("  1. Configure CodeRabbit: coderabbit configure (if not done)")
            print("  2. Customize .coderabbit.yaml to your needs")
            print("  3. Start coding!")
        print("\n💡 Tip: Edit templates in", self.templates_dir, "to customize future projects")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialize a new project with git and CodeRabbit CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize in current directory with Python defaults
  %(prog)s
  
  # Initialize in specific directory
  %(prog)s --path ~/projects/my-new-project
  
  # Use generic .gitignore
  %(prog)s --language generic
  
  # Skip README and workflow explanation
  %(prog)s --no-readme --no-workflow
  
  # Use custom templates directory
  %(prog)s --templates-dir ~/.config/project-templates
        """
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Project path (default: current directory)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="python",
        help="Programming language for .gitignore template (default: python)"
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=None,
        help="Custom templates directory (default: ./templates)"
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="Skip README.md creation"
    )
    parser.add_argument(
        "--no-workflow",
        action="store_true",
        help="Skip workflow explanation"
    )
    
    args = parser.parse_args()
    
    initializer = ProjectInitializer(args.path, args.templates_dir)
    initializer.run(
        language=args.language,
        create_readme=not args.no_readme,
        explain_workflow=not args.no_workflow
    )


if __name__ == "__main__":
    main()
