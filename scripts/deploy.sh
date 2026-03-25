#!/usr/bin/env bash
# deploy.sh — Build and publish the emergent package to PyPI using uv.
#
# Usage:
#   ./scripts/deploy.sh [--test]        # publish to TestPyPI
#   ./scripts/deploy.sh                 # publish to PyPI
#
# Prerequisites:
#   - uv >= 0.4.0  (https://docs.astral.sh/uv/)
#   - PYPI_TOKEN env var set (or UV_PUBLISH_TOKEN)
#   - Optionally TEST_PYPI_TOKEN for --test publishes

set -euo pipefail

# ── Colours ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[deploy]${NC} $*"; }
warn()  { echo -e "${YELLOW}[deploy]${NC} $*"; }
error() { echo -e "${RED}[deploy] ERROR:${NC} $*" >&2; exit 1; }

# ── Options ────────────────────────────────────────────────────────────────────
TEST_PYPI=false
for arg in "$@"; do
  case $arg in
    --test) TEST_PYPI=true ;;
    *) error "Unknown argument: $arg" ;;
  esac
done

# ── Root of the repo ──────────────────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ── Load .env / .env.local (existing env vars take precedence) ────────────────
_load_env_file() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue       # skip comments
    [[ -z "${line//[[:space:]]/}" ]] && continue      # skip blank lines
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
      local varname="${BASH_REMATCH[1]}"
      local varval="${BASH_REMATCH[2]}"
      # Strip surrounding single or double quotes
      [[ "$varval" =~ ^\"(.*)\"$ ]] && varval="${BASH_REMATCH[1]}"
      [[ "$varval" =~ ^\'(.*)\'$ ]] && varval="${BASH_REMATCH[1]}"
      # Only set if not already exported in the environment (bash 3.2 compatible)
      [[ -n "${!varname+x}" ]] || export "$varname=$varval"
    fi
  done < "$file"
}
_load_env_file "$REPO_ROOT/.env"
_load_env_file "$REPO_ROOT/.env.local"

# ── Verify uv is available ────────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
  error "uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

UV_VERSION=$(uv --version | awk '{print $2}')
info "Using uv $UV_VERSION"

# ── Check for a clean git working tree ───────────────────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
  warn "Working tree is not clean. Uncommitted changes will NOT be included in the build."
  read -rp "Continue anyway? [y/N] " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || exit 1
fi

# ── Read current version from pyproject.toml ─────────────────────────────────
VERSION=$(grep '^version' pyproject.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')
info "Building version: $VERSION"

# ── Clean previous dist artefacts ────────────────────────────────────────────
if [[ -d dist ]]; then
  info "Removing old dist/ directory…"
  rm -rf dist
fi

# ── Build (sdist + wheel) ─────────────────────────────────────────────────────
info "Building source distribution and wheel…"
uv build

# List what was built
echo ""
info "Build artefacts:"
ls -lh dist/
echo ""

# ── Publish ───────────────────────────────────────────────────────────────────
if $TEST_PYPI; then
  info "Publishing to TestPyPI…"
  : "${TEST_PYPI_TOKEN:?TEST_PYPI_TOKEN env var must be set for --test publishes}"
  if ! uv publish \
    --publish-url https://test.pypi.org/legacy/ \
    --token "$TEST_PYPI_TOKEN"; then
    error "Publish to TestPyPI failed for version $VERSION.
  Common causes:
    - Version $VERSION already exists on TestPyPI (bump version in pyproject.toml)
    - Invalid or expired TEST_PYPI_TOKEN
  Check: https://test.pypi.org/project/emergent/$VERSION/"
  fi
  info "Done! Verify at: https://test.pypi.org/project/emergent/$VERSION/"
else
  info "Publishing to PyPI…"
  : "${PYPI_TOKEN:?PYPI_TOKEN env var must be set. Create one at https://pypi.org/manage/account/token/}"
  if ! uv publish --token "$PYPI_TOKEN"; then
    error "Publish to PyPI failed for version $VERSION.
  Common causes:
    - Version $VERSION already exists on PyPI (bump version in pyproject.toml)
    - Invalid or expired PYPI_TOKEN
  Check: https://pypi.org/project/emergent/$VERSION/"
  fi
  info "Done! View at: https://pypi.org/project/emergent/$VERSION/"
fi
