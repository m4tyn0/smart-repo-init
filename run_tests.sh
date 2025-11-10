#!/bin/bash
# Run all unit tests for smart-repo-init

set -e

echo "🧪 Running unit tests with uv..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found. Installing uv..."
    echo "   Run: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "   Falling back to pip for this run..."

    # Fallback to pip if uv is not available
    if ! command -v pytest &> /dev/null; then
        echo "   Installing test dependencies with pip..."
        pip install -r requirements-test.txt
    fi
    pytest tests/ -v
else
    echo "✅ Using uv for fast dependency management"

    # Sync dependencies with uv (this is much faster than pip)
    uv sync --extra test

    # Run tests with uv
    uv run pytest tests/ -v
fi

echo ""
echo "✅ All tests completed!"
