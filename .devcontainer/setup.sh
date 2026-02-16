#!/bin/bash
set -e

echo "🚀 Setting up development environment..."

# Install uv
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Add uv to shell profile for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true

# Install Claude Code CLI 
echo "🤖 Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

# Install project dependencies with uv (including dev dependencies)
echo "📚 Installing project dependencies..."
uv sync --extra dev

# Add activation helper to shell profile
echo 'alias activate-venv="source .venv/bin/activate"' >> ~/.bashrc
echo 'alias activate-venv="source .venv/bin/activate"' >> ~/.zshrc 2>/dev/null || true

echo "✅ Development environment setup complete!"
echo ""
echo "💡 Quick tips:"
echo "   - uv is ready to use: 'uv --help'"
if [ "${INSTALL_CLAUDE_CODE:-false}" = "true" ]; then
  echo "   - Claude Code is available: 'claude --help'"
fi
echo "   - Python venv is at .venv/ (auto-activated in VS Code/Cursor)"
echo "   - Run 'activate-venv' in terminal to manually activate the venv"
