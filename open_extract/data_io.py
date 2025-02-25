from pathlib import Path


def load_md(path: Path) -> str:
    """Load md from file."""

    with open(path, "r") as f:
        return f.read()
