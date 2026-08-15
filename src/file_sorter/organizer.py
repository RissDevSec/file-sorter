"""Core file organization logic."""

from __future__ import annotations

import shutil
from pathlib import Path

from .categories import categorize


def organize(folder: Path) -> None:
    """Move every file in *folder* into a category subfolder."""
    for entry in sorted(folder.iterdir(), key=lambda path: path.name.lower()):
        if not entry.is_file():
            continue

        category = categorize(entry.suffix)
        target_folder = folder / category
        target_folder.mkdir(parents=True, exist_ok=True)

        shutil.move(entry, target_folder / entry.name)
        print(f"Moved: {entry.name} -> {category}/")
