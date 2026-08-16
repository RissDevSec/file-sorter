"""Core file organization logic."""

from __future__ import annotations

import shutil
from pathlib import Path

from .categories import categorize


def unique_destination(folder: Path, filename: str) -> Path:
    """Return a destination path that does not overwrite an existing file."""
    destination = folder / filename
    if not destination.exists():
        return destination

    original = Path(filename)
    counter = 1
    while True:
        candidate = folder / f"{original.stem} ({counter}){original.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path) -> None:
    """Move every file in *folder* into a category subfolder."""
    for entry in sorted(folder.iterdir(), key=lambda path: path.name.lower()):
        if not entry.is_file():
            continue

        category = categorize(entry.suffix)
        target_folder = folder / category
        target_folder.mkdir(parents=True, exist_ok=True)
        destination = unique_destination(target_folder, entry.name)

        shutil.move(entry, destination)
        print(f"Moved: {entry.name} -> {category}/{destination.name}")
