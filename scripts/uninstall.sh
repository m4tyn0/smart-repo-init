#!/bin/bash
# Uninstall script for smart-repo-init tools

set -e

echo "🗑️  Uninstalling smart-repo-init tools..."
echo ""

# Detect shell
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

# Remove installed scripts
removed_count=0

if [ -f "$HOME/bin/project-init" ]; then
    rm "$HOME/bin/project-init"
    echo "✅ Removed ~/bin/project-init"
    ((removed_count++))
fi

if [ -f "$HOME/bin/project-init-full" ]; then
    rm "$HOME/bin/project-init-full"
    echo "✅ Removed ~/bin/project-init-full"
    ((removed_count++))
fi

# Remove templates directory
if [ -d "$HOME/bin/templates" ]; then
    rm -rf "$HOME/bin/templates"
    echo "✅ Removed ~/bin/templates"
    ((removed_count++))
fi

# Check if ~/bin is empty and remove it
if [ -d "$HOME/bin" ] && [ -z "$(ls -A $HOME/bin)" ]; then
    rmdir "$HOME/bin"
    echo "✅ Removed empty ~/bin directory"

    # Remove PATH addition from shell config
    if [ -n "$SHELL_CONFIG" ]; then
        if grep -q '# Added by smart-repo-init installer' "$SHELL_CONFIG"; then
            # Create a temporary file without the PATH export
            grep -v '# Added by smart-repo-init installer' "$SHELL_CONFIG" | \
            grep -v 'export PATH="$HOME/bin:$PATH"' > "$SHELL_CONFIG.tmp"
            mv "$SHELL_CONFIG.tmp" "$SHELL_CONFIG"
            echo "✅ Removed PATH modification from $SHELL_CONFIG"
        fi
    fi
fi

echo ""
if [ $removed_count -eq 0 ]; then
    echo "ℹ️  No smart-repo-init tools found to uninstall"
else
    echo "🎉 Uninstallation complete!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Restart your terminal or run: source $SHELL_CONFIG"
    echo "  2. The project directory is still available if you want to reinstall later"
fi
echo ""
