"""Command-line entry point for file-sorter."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .organizer import OrganizeResult, organize


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="file-sorter",
        description="Sort files into category folders based on their extensions.",
    )
    parser.add_argument(
        "folder",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="folder to organize (default: ~/Downloads)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def print_result(result: OrganizeResult) -> None:
    """Print a human-readable summary of an organize run."""
    for source, destination in result.moved:
        print(f"Moved: {source.name} -> {destination.parent.name}/{destination.name}")

    for source in result.skipped:
        print(f"Skipped: {source.name}")

    for source, error in result.failed:
        print(f"Failed: {source.name}: {error}")

    print(
        f"Done. {len(result.moved)} moved, "
        f"{len(result.skipped)} skipped, {len(result.failed)} failed."
    )


def main(argv: list[str] | None = None) -> int:
    """Run the organizer and return a process exit code."""
    args = build_parser().parse_args(argv)
    folder = args.folder.expanduser()

    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        return 1

    result = organize(folder)
    print_result(result)
    return 1 if result.failed else 0
