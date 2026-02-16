# Contributing to Emergent

Thank you for considering contributing to the **Emergent** project! We value your input and collaboration to make this package better for everyone. Below are the guidelines to help you get started and ensure smooth contributions.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Code Contributions](#code-contributions)
3. [Documentation](#documentation)

---

## **Getting Started**

### **1. Fork and Clone**

1. Fork the repository to your GitHub account: [Fork emergent](https://github.com/delphilos/emergent/fork)
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/emergent.git
   cd emergent
   ```
3. Add the upstream repository as a remote:
   ```bash
   git remote add upstream https://github.com/delphilos/emergent.git
   ```

### **2. Setup Development Environment**

**Local Setup (Without Container)**

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management.

1. Install uv:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or use Homebrew
   brew install uv
   ```

2. Install dependencies (including dev tools):
   ```bash
   # Install all dependencies including dev tools
   uv sync --extra dev

   # Or install only core dependencies
   uv sync
   ```

**Using Dev Container**

This project includes a dev container for a consistent development environment with uv pre-installed.

1. Install Docker and VS Code/Cursor with the Dev Containers extension ([setup guide](https://code.visualstudio.com/docs/devcontainers/containers#_installation))
2. Open the project in your editor
3. When prompted, click "Reopen in Container"
4. All dependencies (including uv and dev tools) will be installed automatically

**Optional**: To install Claude Code CLI in the devcontainer, set `"INSTALL_CLAUDE_CODE": "true"` in the `remoteEnv` section of `.devcontainer/devcontainer.json`

---

## **Code Contributions**

### **1. Create a Branch**

Create a new branch for your work:
```bash
git checkout -b <your-github-username>/<your-feature-name>
```

### **2. Make Your Changes**

- Write clean, modular code with meaningful variable and function names
- Follow [PEP 8](https://pep8.org/) guidelines for Python code style
- Add tests for new functionality when appropriate

### **3. Commit Your Changes**

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for clear and consistent commit messages.

**Format**: `type(optional-scope): description`

**Common types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `build:` - Build system or dependency changes
- `ci:` - CI/CD configuration changes

**Scope** (optional): Use parentheses to specify the area of change (e.g., `api`, `cli`, `deps`, `agents`).

**Examples**:
```bash
# Without scope
git commit -m "feat: add graph visualization function"
git commit -m "fix: correct agent parameter validation"
git commit -m "docs: update installation instructions"

# With scope
git commit -m "feat(agents): add support for custom behavior functions"
git commit -m "fix(cli): resolve argument parsing error"
git commit -m "chore(deps): update numpy to 2.4.1"
```

### **4. Push and Create Pull Request**

1. Push your branch to your fork:
   ```bash
   git push origin <your-github-username>/<your-feature-name>
   ```

2. Open a pull request:
   - Go to [github.com/delphilos/emergent](https://github.com/delphilos/emergent)
   - Click "Pull requests" → "New pull request"
   - Click "compare across forks" and select your fork and branch
   - Provide a detailed description of your changes
   - Link any related issues

3. Address feedback from maintainers and update your PR as needed

### **5. Keep Your Fork Updated**

Sync your fork with the upstream repository regularly:
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## **Documentation**
Documentation is essential for both developers working on the `emergent` codebase and users of the package. 

Internal documentation should be located in close proximity to the code in docstrings and module README files, while external user-facing documentation should be located in the `docs` directory.

### **Internal Documentation**
1. **Docstrings**: Include detailed docstrings for all public classes, methods, and functions:
   ```python
   def example_function(param1, param2):
       """
       This function demonstrates an example.

       Args:
           param1 (int): Description of param1.
           param2 (str): Description of param2.

       Returns:
           bool: True if successful, False otherwise.

       Notes:
           Additional internal details for developers.
       """
       pass
   ```
2. **README Files in Subdirectories**: When needed, include a `README.md` file in directories for more detailed documentation about the code within.

### **External Documentation**
1. **Location**: All user-facing documentation resides in the `docs/` directory.
2. **Format**: Use Markdown (`.md`) for all documents unless otherwise specified.
3. **Organization**: Ensure documentation is placed in the appropriate section, e.g., installation instructions in `installation.md` and usage examples in `usage.md`.
4. **Content Standards**:
   - Use simple, jargon-free language.
   - Include code examples whenever possible.
   - Provide clear explanations of all features and APIs.

### **Editing Documentation**
1. Update the appropriate files (either alongside code in `src/` or in the `docs/` directory).
2. Use consistent formatting and adhere to existing styles.
3. If you add a new feature, include it in both internal and external documentation as appropriate.

---

Thank you for contributing! Your efforts make **Emergent** a better tool for everyone. 🚀

