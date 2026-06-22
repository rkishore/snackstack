# SnackStack

Agentic AI snack-ordering assistant.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.
Python 3.12 is pinned via `.python-version` (uv downloads it automatically).

```bash
# Install / refresh the environment (creates .venv and reads uv.lock)
uv sync

# Add or remove dependencies (updates pyproject.toml and uv.lock)
uv add <package>
uv add --dev <package>     # dev-only tools (linters, test runners, ...)
uv remove <package>

# Run commands inside the project environment
uv run python -m snackstack.main
uv run <command>
```

Commit `pyproject.toml`, `uv.lock`, and `.python-version`. The `.venv/`
directory is git-ignored and recreated by `uv sync`.
