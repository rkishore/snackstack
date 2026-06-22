"""Console entry point for the snackstack application."""

def main() -> int:
    """Run the snackstack application.
    
    Wired to the `snackstack` command via [project.scripts] in pyproject.toml.
    Returns an exit code (0 = success)
    """
    print("Running snackstack application...")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
