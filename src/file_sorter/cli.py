"""Command-line entry point for file-sorter."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .organizer import organize


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


def main(argv: list[str] | None = None) -> int:
    """Run the organizer and return a process exit code."""
    args = build_parser().parse_args(argv)
    folder = args.folder.expanduser()

    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        return 1

    organize(folder)
    print("Selesai merapikan folder")
    return 0
