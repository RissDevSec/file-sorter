"""Core file organization logic."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from .categories import categorize

IGNORED_NAMES: Final[frozenset[str]] = frozenset({"desktop.ini"})
IGNORED_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {".crdownload", ".part", ".tmp"}
)


@dataclass
class OrganizeResult:
    """Summary of an organize run."""

    moved: list[tuple[Path, Path]] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    failed: list[tuple[Path, OSError]] = field(default_factory=list)


def should_skip(path: Path) -> bool:
    """Return True for hidden files and unfinished downloads."""
    return (
        path.name.startswith(".")
        or path.name in IGNORED_NAMES
        or path.suffix.lower() in IGNORED_EXTENSIONS
    )


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


def move_file(source: Path, folder: Path) -> Path:
    """Move one file into its category folder and return the new path."""
    category = categorize(source.suffix)
    target_folder = folder / category
    target_folder.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(target_folder, source.name)

    shutil.move(source, destination)
    return destination


def organize(folder: Path) -> OrganizeResult:
    """Move files in *folder* into category subfolders.

    A failure on one file is recorded and does not stop the remaining
    files from being processed.
    """
    result = OrganizeResult()

    for entry in sorted(folder.iterdir(), key=lambda path: path.name.lower()):
        if not entry.is_file():
            continue

        if should_skip(entry):
            result.skipped.append(entry)
            continue

        try:
            destination = move_file(entry, folder)
        except OSError as error:
            result.failed.append((entry, error))
        else:
            result.moved.append((entry, destination))

    return result
