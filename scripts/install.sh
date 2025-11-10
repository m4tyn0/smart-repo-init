
#!/bin/bash
# Installation script for smart-repo-init tools

set -e

echo "🚀 Installing smart-repo-init tools..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📍 Script location: $SCRIPT_DIR"
echo "📍 Project root: $PROJECT_ROOT"
echo ""

# Detect shell
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "⚠️  Could not detect shell config file"
    echo "Please manually add ~/bin to your PATH"
fi

# Create bin directory
mkdir -p "$HOME/bin"
echo "✅ Created ~/bin directory"

# Copy scripts from scripts/ directory
if [ -f "$SCRIPT_DIR/quick_init_project.py" ]; then
    cp "$SCRIPT_DIR/quick_init_project.py" "$HOME/bin/project-init"
    chmod +x "$HOME/bin/project-init"
    echo "✅ Copied quick_init_project.py to ~/bin/project-init"
else
    echo "❌ Error: Could not find quick_init_project.py in $SCRIPT_DIR"
    exit 1
fi

if [ -f "$SCRIPT_DIR/full_init_project.py" ]; then
    cp "$SCRIPT_DIR/full_init_project.py" "$HOME/bin/project-init-full"
    chmod +x "$HOME/bin/project-init-full"
    echo "✅ Copied full_init_project.py to ~/bin/project-init-full"
else
    echo "❌ Error: Could not find full_init_project.py in $SCRIPT_DIR"
    exit 1
fi

# Copy templates from templates/ directory
if [ -d "$PROJECT_ROOT/templates" ]; then
    cp -r "$PROJECT_ROOT/templates" "$HOME/bin/templates"
    echo "✅ Copied templates to ~/bin/templates"
else
    echo "❌ Error: Could not find templates directory at $PROJECT_ROOT/templates"
    exit 1
fi

# Add to PATH if not already there
if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo '# Added by smart-repo-init installer' >> "$SHELL_CONFIG"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_CONFIG"
        echo "✅ Added ~/bin to PATH in $SHELL_CONFIG"
        echo ""
        echo "⚠️  Run: source $SHELL_CONFIG"
        echo "   Or restart your terminal"
    else
        echo "✅ PATH already configured"
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  project-init           # Quick setup with defaults"
echo "  project-init-full      # Full setup with options"
echo ""
echo "Next steps:"
echo "  1. Reload your shell: source $SHELL_CONFIG"
echo "  2. Install CodeRabbit CLI:"
echo "     curl -fsSL https://cli.coderabbit.ai/install.sh | sh"
echo ""
echo "  3. Create a new project:"
echo "     mkdir myproject && cd myproject && project-init"
echo ""