#!/bin/bash
set -e
echo "🚀 Hermes Quick Setup"
echo ""

# Create venv
if [ ! -d "venv" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
    export PATH="$HOME/.local/bin:$PATH"
    uv venv venv --python 3.11
fi

source venv/bin/activate
pip install -e ".[web]" 2>/dev/null

# Build dashboard
if command -v npm &>/dev/null; then
    cd web && npm install --silent 2>/dev/null && npx vite build 2>/dev/null && cd ..
    echo "✅ Dashboard built"
fi

# Install custom skills
SKILL_DIR="$HOME/.hermes/skills"
mkdir -p "$SKILL_DIR"
cp -r skills/custom/* "$SKILL_DIR/" 2>/dev/null

# Migrate from OpenClaw
if [ -d "$HOME/.openclaw" ]; then
    hermes claw migrate --preset full --overwrite --yes 2>/dev/null
    echo "✅ OpenClaw migrated"
fi

echo ""
echo "✅ Setup complete!"
echo "  ./start-chat.sh       — CLI chat"
echo "  ./start-dashboard.sh  — Web dashboard (http://127.0.0.1:9119)"
echo "  hermes setup          — Configure model & API keys"
