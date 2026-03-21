# Deploy Scripts

This directory contains scripts for building and publishing the `emergent` package to [PyPI](https://pypi.org/project/emergent/).

## Prerequisites

### 1. Install uv

[uv](https://docs.astral.sh/uv/) is the package manager used for building and publishing.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:

```bash
uv --version  # should be >= 0.4.0
```

### 2. Create a PyPI API token

1. Log in to [pypi.org](https://pypi.org) (or [test.pypi.org](https://test.pypi.org) for test publishes).
2. Go to **Account Settings → API tokens → Add API token**.
3. Scope the token to the `emergent` project for least-privilege access.
4. Copy the token — it starts with `pypi-`.

Export it in your shell (or add to your `.env` / secret manager):

```bash
export PYPI_TOKEN="pypi-..."
# for TestPyPI publishes:
export TEST_PYPI_TOKEN="pypi-..."
```

> **Never commit tokens to version control.**

---

## deploy.sh

Builds the package and publishes it to PyPI in one step.

### What it does

1. Verifies `uv` is installed.
2. Warns if the git working tree has uncommitted changes.
3. Reads the current version from `pyproject.toml`.
4. Removes any stale `dist/` artefacts.
5. Runs `uv build` to produce an sdist (`.tar.gz`) and a wheel (`.whl`).
6. Runs `uv publish` to upload both artefacts to PyPI (or TestPyPI).

### Usage

**Publish to TestPyPI first (recommended)**

```bash
export TEST_PYPI_TOKEN="pypi-..."
./scripts/deploy.sh --test
```

Install from TestPyPI to verify the release looks correct:

```bash
uv pip install --index-url https://test.pypi.org/simple/ emergent==<version>
```

**Publish to PyPI**

```bash
export PYPI_TOKEN="pypi-..."
./scripts/deploy.sh
```

---

## Bumping the version

Update the `version` field in `pyproject.toml` before running the deploy script:

```toml
[project]
version = "0.1.0"   # <-- bump this
```

Create a release branch and open a PR — do **not** push version bumps or release tags directly to `main`:

```bash
git checkout -b release/v0.1.0
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push origin release/v0.1.0
# open a PR → merge into main via GitHub
```

After the PR is merged, tag the release from `main`:

```bash
git checkout main && git pull
git tag v0.1.0
git push origin v0.1.0
```

Then run the deploy script.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `PYPI_TOKEN env var must be set` | Export your PyPI API token (see above) |
| `File already exists` (HTTP 400) | You cannot re-upload the same version. Bump the version number. |
| Build fails with missing metadata | Ensure `pyproject.toml` has all required fields (`name`, `version`, `readme`, etc.) |