# UV Guide for Claude Code Sessions

## IMPORTANT: Always Use uv Instead of pip

This guide ensures Claude Code consistently uses `uv` for Python package management. **Always check for and use `uv` before falling back to pip.**

## Quick Reference - Essential Commands

### Starting a New Project
```bash
# ALWAYS do this first for new Python projects
uv init
uv add [packages]  # Instead of pip install
uv run main.py    # Instead of python main.py
```

### Working with Existing Projects
```bash
# If project has pyproject.toml or requirements.txt
uv sync           # Installs all dependencies
uv run [command]  # Runs commands in project environment
```

## Command Replacements - MEMORIZE THESE

| ❌ DON'T USE | ✅ USE INSTEAD |
|--------------|----------------|
| `pip install package` | `uv add package` or `uv pip install package` |
| `pip install -e .` | `uv pip install -e .` or `uv sync` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `python -m venv venv` | `uv venv` |
| `python script.py` | `uv run script.py` |
| `python -m pytest` | `uv run pytest` |
| `pip list` | `uv pip list` |
| `pip freeze` | `uv pip freeze` |

## Standard Workflow for Claude Code

### 1. Check if uv is installed
```bash
uv --version
```
If not installed, inform user to install it via:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. For New Projects
```bash
# Create project structure
uv init project-name
cd project-name

# Add dependencies
uv add click rich groq  # Example packages

# Run code
uv run main.py
```

### 3. For Existing Projects with pyproject.toml
```bash
# Sync all dependencies
uv sync

# Add new dependency
uv add new-package

# Run in environment
uv run python script.py
```

### 4. For Projects with requirements.txt
```bash
# Create virtual environment
uv venv

# Install from requirements
uv pip install -r requirements.txt

# Or convert to pyproject.toml workflow
uv init
uv add -r requirements.txt
```

## Windows-Specific Reminders

### Virtual Environment Activation (if needed)
```bash
# Usually NOT needed with uv run, but if explicitly required:
.venv\Scripts\activate       # Command Prompt
.venv\Scripts\Activate.ps1   # PowerShell
```

### Path Handling
- uv handles paths automatically
- No need to modify PATH manually
- Works with both forward and backward slashes

## Common Scenarios

### Installing Development Dependencies
```bash
# Add as dev dependency
uv add --dev pytest black flake8

# Install including dev dependencies
uv sync --dev
```

### Running Tests
```bash
# Instead of: python -m pytest
uv run pytest

# With coverage
uv run pytest --cov
```

### Building Package
```bash
# Instead of: python -m build
uv build
```

### Installing Editable Package
```bash
# For development mode installation
uv pip install -e .
# OR better:
uv sync  # If project has pyproject.toml
```

## Troubleshooting Guide

### If Dependencies Conflict
```bash
# Clear and rebuild environment
rm -rf .venv  # or manually delete .venv folder on Windows
uv sync
```

### If Package Not Found
```bash
# Check if in virtual environment
uv pip list

# Force reinstall
uv pip install --force-reinstall package-name
```

### If SSL/Certificate Issues
```bash
# Use system certificates
uv pip install --native-tls package-name
```

## Project Structure with uv

When creating new projects, uv creates:
```
project/
├── .gitignore
├── .python-version    # Pins Python version
├── README.md
├── pyproject.toml     # Dependencies and metadata
├── uv.lock           # Lockfile for reproducibility
└── main.py           # Entry point
```

## Key Benefits to Mention to Users

1. **Speed**: 10-100x faster than pip
2. **No activation needed**: `uv run` handles environment automatically
3. **Reproducible**: `uv.lock` ensures same versions everywhere
4. **Cleaner**: No global package pollution
5. **Modern**: Built for modern Python workflows

## CRITICAL REMINDERS

1. **ALWAYS use `uv run`** to execute Python scripts in projects
2. **ALWAYS use `uv add`** instead of pip install for new dependencies
3. **ALWAYS check for `pyproject.toml`** and use `uv sync` if it exists
4. **NEVER mix pip and uv** in the same virtual environment
5. **ALWAYS suggest uv** for new Python projects

## Example Session Start

When starting work on a Python project:
```bash
# First, check for uv
uv --version

# If pyproject.toml exists
uv sync
uv run python --version

# If new project
uv init
uv add needed-packages

# Always run code with
uv run script.py
```

## Quick Decision Tree

```
Is this a Python project?
├─ Yes
│  ├─ Is uv installed?
│  │  ├─ Yes → Use uv commands
│  │  └─ No → Suggest installation
│  ├─ Has pyproject.toml?
│  │  ├─ Yes → uv sync
│  │  └─ No → uv init or uv venv
│  └─ Running code?
│     └─ Use: uv run [command]
└─ No → Use appropriate tools
```

Remember: uv is the preferred Python package manager for all projects!