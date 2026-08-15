"""Command-line entry point for file-sorter."""

from __future__ import annotations

from pathlib import Path

from .organizer import organize


def main() -> int:
    """Organize the user's Downloads folder."""
    folder = Path.home() / "Downloads"

    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        return 1

    organize(folder)
    print("Selesai merapikan folder")
    return 0
