#!/bin/bash
# Run all unit tests for smart-repo-init

set -e

echo "🧪 Running unit tests..."
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "⚠️  pytest not found. Installing test dependencies..."
    pip install -r requirements-test.txt
fi

# Run tests with pytest
pytest tests/ -v

echo ""
echo "✅ All tests completed!"
