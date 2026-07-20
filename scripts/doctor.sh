#!/usr/bin/env bash

set -e

echo ""
echo "=========================================="
echo " FamilyOS CLI Doctor"
echo "=========================================="
echo ""

echo "📍 Working directory"
pwd
echo ""

echo "🌿 Git status"
git status --short
echo ""

echo "📂 Project structure"
tree -L 2 -I "__pycache__|.pytest_cache|.ruff_cache|.venv"
echo ""

echo "🐍 Python package"
tree src/familyos_cli -L 4 -I "__pycache__"
echo ""

echo "📄 Templates"
tree templates
echo ""

echo "📑 Specifications"
tree specifications
echo ""

echo "🧹 Ruff"
ruff check .
echo ""

echo "🧪 Pytest"
pytest
echo ""

echo "⚙️ CLI Help"
familyos --help
echo ""

echo "📦 CLI Version"
familyos version
echo ""

echo "🧱 Demo Project"

rm -rf demo

familyos init demo

tree demo

echo ""

echo "📄 README"

cat demo/README.md

echo ""

echo "=========================================="
echo "✅ FamilyOS Doctor completed successfully"
echo "=========================================="