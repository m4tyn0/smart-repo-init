#!/usr/bin/env python3
"""
Interactive TUI Project Initialization Script
A beautiful terminal interface for setting up new projects with CodeRabbit CLI.
"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import json

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align
    from rich import box
    from rich.live import Live
    from rich.status import Status
except ImportError:
    print("❌ Rich library not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align
    from rich import box
    from rich.live import Live
    from rich.status import Status


class ProjectInitializerTUI:
    def __init__(self, project_path: Path = Path.cwd(), templates_dir: Optional[Path] = None):
        self.console = Console()
        self.project_path = project_path
        
        # Find templates directory
        if templates_dir is None:
            script_dir = Path(__file__).parent
            self.templates_dir = script_dir / "templates"
            if not self.templates_dir.exists():
                self.templates_dir = Path.cwd() / "templates"
        else:
            self.templates_dir = templates_dir
            
        if not self.templates_dir.exists():
            self.console.print("⚠️  Templates directory not found, creating basic templates...", style="yellow")
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
    
    def show_welcome(self) -> None:
        """Display welcome screen."""
        welcome_text = """
🚀 Smart Repository Initializer

Welcome to the interactive project setup wizard!
This tool will help you initialize a new project with:
• Git repository setup
• Language-specific .gitignore files
• CodeRabbit CLI integration
• Pre-commit hooks
• Docker support
• And much more!
        """
        
        panel = Panel(
            welcome_text.strip(),
            title="[bold blue]Welcome[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def get_project_info(self) -> Dict[str, Any]:
        """Gather project information from user."""
        self.console.print("[bold cyan]📋 Project Information[/bold cyan]")
        self.console.print()
        
        # Project name
        project_name = Prompt.ask(
            "[bold]Project name[/bold]",
            default=self.project_path.name
        )
        
        # Project description
        description = Prompt.ask(
            "[bold]Project description[/bold]",
            default="A new project"
        )
        
        # Programming language
        language_table = Table(title="Available Languages", box=box.ROUNDED)
        language_table.add_column("Option", style="cyan", no_wrap=True)
        language_table.add_column("Language", style="magenta")
        language_table.add_column("Description", style="white")
        
        languages = {
            "1": ("python", "Python", "Python project with virtual environment support"),
            "2": ("javascript", "JavaScript", "Node.js/JavaScript project"),
            "3": ("typescript", "TypeScript", "TypeScript project"),
            "4": ("java", "Java", "Java project with Maven/Gradle"),
            "5": ("go", "Go", "Go project"),
            "6": ("rust", "Rust", "Rust project"),
            "7": ("generic", "Generic", "Generic project (minimal setup)")
        }
        
        for key, (value, name, desc) in languages.items():
            language_table.add_row(key, name, desc)
        
        self.console.print(language_table)
        self.console.print()
        
        language_choice = Prompt.ask(
            "[bold]Select programming language[/bold]",
            choices=list(languages.keys()),
            default="1"
        )
        selected_language = languages[language_choice][0]
        
        return {
            "name": project_name,
            "description": description,
            "language": selected_language
        }
    
    def get_setup_options(self) -> Dict[str, bool]:
        """Get setup options from user."""
        self.console.print("[bold cyan]⚙️  Setup Options[/bold cyan]")
        self.console.print()
        
        options = {
            "create_readme": Confirm.ask(
                "[bold]Create README.md[/bold]",
                default=True
            ),
            "setup_docker": Confirm.ask(
                "[bold]Add Docker support[/bold]",
                default=False
            ),
            "setup_precommit": Confirm.ask(
                "[bold]Setup pre-commit hooks[/bold]",
                default=True
            ),
            "setup_coderabbit": Confirm.ask(
                "[bold]Setup CodeRabbit CLI[/bold]",
                default=True
            ),
            "create_initial_commit": Confirm.ask(
                "[bold]Create initial commit[/bold]",
                default=True
            ),
            "explain_workflow": Confirm.ask(
                "[bold]Show workflow explanation[/bold]",
                default=True
            )
        }
        
        return options
    
    def check_prerequisites(self) -> Dict[str, bool]:
        """Check system prerequisites."""
        self.console.print("[bold cyan]🔍 Checking Prerequisites[/bold cyan]")
        self.console.print()
        
        checks = {}
        
        # Check Git
        git_available = shutil.which("git") is not None
        checks["git"] = git_available
        status = "✅" if git_available else "❌"
        self.console.print(f"{status} Git: {'Available' if git_available else 'Not found'}")
        
        # Check CodeRabbit CLI
        coderabbit_available = shutil.which("coderabbit") is not None
        checks["coderabbit"] = coderabbit_available
        status = "✅" if coderabbit_available else "⚠️"
        self.console.print(f"{status} CodeRabbit CLI: {'Installed' if coderabbit_available else 'Not installed'}")
        
        # Check if folder is empty
        files = [f for f in self.project_path.iterdir() if not f.name.startswith('.')]
        folder_empty = len(files) == 0
        checks["folder_empty"] = folder_empty
        status = "✅" if folder_empty else "⚠️"
        self.console.print(f"{status} Project folder: {'Empty' if folder_empty else 'Contains files'}")
        
        # Check Git configuration
        try:
            result = subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True,
                text=True,
                check=True
            )
            git_configured = bool(result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            git_configured = False
        
        checks["git_configured"] = git_configured
        status = "✅" if git_configured else "⚠️"
        self.console.print(f"{status} Git user: {'Configured' if git_configured else 'Not configured'}")
        
        self.console.print()
        return checks
    
    def show_summary(self, project_info: Dict[str, Any], options: Dict[str, bool]) -> bool:
        """Show setup summary and confirm."""
        self.console.print("[bold cyan]📊 Setup Summary[/bold cyan]")
        self.console.print()
        
        summary_table = Table(box=box.ROUNDED)
        summary_table.add_column("Setting", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="white")
        
        summary_table.add_row("Project Name", project_info["name"])
        summary_table.add_row("Description", project_info["description"])
        summary_table.add_row("Language", project_info["language"].title())
        summary_table.add_row("Path", str(self.project_path))
        
        self.console.print(summary_table)
        self.console.print()
        
        # Options table
        options_table = Table(title="Setup Options", box=box.ROUNDED)
        options_table.add_column("Option", style="cyan")
        options_table.add_column("Status", style="white")
        
        for option, enabled in options.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            option_name = option.replace("_", " ").title()
            options_table.add_row(option_name, status)
        
        self.console.print(options_table)
        self.console.print()
        
        return Confirm.ask("[bold]Proceed with setup?[/bold]", default=True)
    
    def run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
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
            self.console.print(f"❌ Command failed: {' '.join(cmd)}", style="red")
            self.console.print(f"Error: {e.stderr}", style="red")
            raise
    
    def copy_template(self, template_name: str, destination: str, replace_vars: Dict[str, str] = None) -> None:
        """Copy a template file from templates directory."""
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            self.console.print(f"⚠️  Template not found: {template_name}", style="yellow")
            return
        
        content = template_path.read_text()
        
        # Replace variables if provided
        if replace_vars:
            for key, value in replace_vars.items():
                content = content.replace(f"{{{key}}}", value)
        
        dest_path = self.project_path / destination
        dest_path.write_text(content)
    
    def setup_git(self) -> bool:
        """Initialize git repository."""
        with Status("Initializing Git repository...", spinner="dots"):
            # Check if git is already initialized
            if (self.project_path / ".git").exists():
                return False
            
            self.run_command(["git", "init"])
            self.run_command(["git", "branch", "-M", "main"])
            return True
    
    def create_gitignore(self, language: str) -> None:
        """Create .gitignore from template."""
        with Status(f"Creating .gitignore for {language}..."):
            template_name = f"gitignore.{language}"
            
            # Fallback to generic if specific template doesn't exist
            if not (self.templates_dir / template_name).exists():
                template_name = "gitignore.generic"
            
            self.copy_template(template_name, ".gitignore")
    
    def create_dockerignore(self) -> None:
        """Create .dockerignore from template."""
        with Status("Creating .dockerignore..."):
            self.copy_template("dockerignore", ".dockerignore")
    
    def create_git_attributes(self) -> None:
        """Create .gitattributes from template."""
        with Status("Creating .gitattributes..."):
            self.copy_template("gitattributes", ".gitattributes")
    
    def setup_precommit_hook(self) -> None:
        """Setup pre-commit hook from template."""
        with Status("Setting up pre-commit hook..."):
            hooks_dir = self.project_path / ".git" / "hooks"
            hooks_dir.mkdir(exist_ok=True)
            
            self.copy_template("pre-commit", ".git/hooks/pre-commit")
            
            # Make executable
            precommit_path = hooks_dir / "pre-commit"
            precommit_path.chmod(0o755)
    
    def setup_coderabbit_cli(self) -> None:
        """Setup CodeRabbit CLI configuration."""
        with Status("Setting up CodeRabbit CLI configuration..."):
            self.copy_template("coderabbit.yaml", ".coderabbit.yaml")
    
    def create_readme(self, project_info: Dict[str, Any]) -> None:
        """Create README.md from template."""
        with Status("Creating README.md..."):
            readme_content = f"""# {project_info['name']}

{project_info['description']}

## Getting Started

This project was initialized with the Smart Repository Initializer.

## Development

### Prerequisites

- Python 3.8+
- Git
- CodeRabbit CLI (optional but recommended)

### Setup

1. Clone the repository
2. Install dependencies (if any)
3. Start developing!

## CodeRabbit Integration

This project is configured with CodeRabbit CLI for automated code reviews.
CodeRabbit will automatically review your commits and provide feedback.

### Installation

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
coderabbit configure
```

### Usage

CodeRabbit will automatically run on each commit via the pre-commit hook.
You can also run it manually:

```bash
coderabbit review
```

## License

[Add your license here]
"""
            
            readme_path = self.project_path / "README.md"
            readme_path.write_text(readme_content)
    
    def create_initial_commit(self) -> None:
        """Create initial commit."""
        with Status("Creating initial commit..."):
            self.run_command(["git", "add", "."])
            self.run_command(["git", "commit", "-m", "Initial commit: Project setup with CodeRabbit CLI"])
    
    def show_workflow_explanation(self) -> None:
        """Show CodeRabbit workflow explanation."""
        workflow_text = """
🐰 CodeRabbit Workflow

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
        """
        
        panel = Panel(
            workflow_text.strip(),
            title="[bold green]CodeRabbit Workflow[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def show_next_steps(self, checks: Dict[str, bool]) -> None:
        """Show next steps after setup."""
        self.console.print("[bold cyan]📋 Next Steps[/bold cyan]")
        self.console.print()
        
        steps = []
        
        if not checks.get("coderabbit"):
            steps.append("1. Install CodeRabbit CLI: curl -fsSL https://cli.coderabbit.ai/install.sh | sh")
            steps.append("2. Configure CodeRabbit: coderabbit configure")
        
        if not checks.get("git_configured"):
            steps.append("Configure Git user:")
            steps.append("  git config --global user.name 'Your Name'")
            steps.append("  git config --global user.email 'you@example.com'")
        
        steps.append("3. Customize .coderabbit.yaml to your needs")
        steps.append("4. Start coding!")
        
        for step in steps:
            self.console.print(f"  {step}")
        
        self.console.print()
        self.console.print("💡 Tip: Edit templates in", str(self.templates_dir), "to customize future projects")
    
    def run(self) -> None:
        """Run the interactive setup process."""
        try:
            # Show welcome
            self.show_welcome()
            
            # Check prerequisites
            checks = self.check_prerequisites()
            
            # Get project information
            project_info = self.get_project_info()
            
            # Get setup options
            options = self.get_setup_options()
            
            # Show summary and confirm
            if not self.show_summary(project_info, options):
                self.console.print("Setup cancelled.", style="yellow")
                return
            
            # Start setup process
            self.console.print()
            self.console.print("[bold green]🚀 Starting Setup...[/bold green]")
            self.console.print()
            
            # Initialize git
            git_initialized = False
            if options.get("setup_precommit", True) or options.get("create_initial_commit", True):
                git_initialized = self.setup_git()
                if git_initialized:
                    self.console.print("✅ Git repository initialized")
            
            # Create .gitignore
            self.create_gitignore(project_info["language"])
            self.console.print("✅ .gitignore created")
            
            # Create .gitattributes
            self.create_git_attributes()
            self.console.print("✅ .gitattributes created")
            
            # Setup Docker support
            if options.get("setup_docker", False):
                self.create_dockerignore()
                self.console.print("✅ .dockerignore created")
            
            # Setup CodeRabbit
            if options.get("setup_coderabbit", True):
                self.setup_coderabbit_cli()
                self.console.print("✅ CodeRabbit configuration created")
            
            # Setup pre-commit hook
            if options.get("setup_precommit", True) and git_initialized:
                self.setup_precommit_hook()
                self.console.print("✅ Pre-commit hook created")
            
            # Create README
            if options.get("create_readme", True):
                self.create_readme(project_info)
                self.console.print("✅ README.md created")
            
            # Create initial commit
            if options.get("create_initial_commit", True) and git_initialized and checks.get("git_configured"):
                self.create_initial_commit()
                self.console.print("✅ Initial commit created")
            elif options.get("create_initial_commit", True) and not checks.get("git_configured"):
                self.console.print("⚠️  Skipping initial commit (Git not configured)", style="yellow")
            
            # Show completion message
            self.console.print()
            completion_panel = Panel(
                "🎉 Project initialization complete!",
                title="[bold green]Success[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(completion_panel)
            
            # Show workflow explanation
            if options.get("explain_workflow", True):
                self.console.print()
                self.show_workflow_explanation()
            
            # Show next steps
            self.console.print()
            self.show_next_steps(checks)
            
        except KeyboardInterrupt:
            self.console.print("\n❌ Setup cancelled by user.", style="red")
        except Exception as e:
            self.console.print(f"\n❌ Setup failed: {e}", style="red")
            raise


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Interactive project initialization with TUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup in current directory
  %(prog)s
  
  # Setup in specific directory
  %(prog)s --path ~/projects/my-new-project
  
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
        "--templates-dir",
        type=Path,
        default=None,
        help="Custom templates directory (default: ./templates)"
    )
    
    args = parser.parse_args()
    
    initializer = ProjectInitializerTUI(args.path, args.templates_dir)
    initializer.run()


if __name__ == "__main__":
    main()
