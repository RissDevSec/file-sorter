"""Extension-to-category mapping used by the organizer."""

from __future__ import annotations

from typing import Final

DEFAULT_CATEGORY: Final[str] = "Other"

FILE_CATEGORIES: Final[dict[str, tuple[str, ...]]] = {
    "Images": (".jpg", ".jpeg", ".png", ".gif"),
    "Documents": (".pdf", ".docx", ".txt", ".xlsx"),
    "Videos": (".mp4", ".mkv", ".mov"),
    "Music": (".mp3", ".wav"),
    "Archives": (".zip", ".rar", ".7z"),
}

EXTENSION_CATEGORIES: Final[dict[str, str]] = {
    extension: category
    for category, extensions in FILE_CATEGORIES.items()
    for extension in extensions
}


def categorize(extension: str) -> str:
    """Return the category for a file extension.

    Extensions are matched case-insensitively. Unknown extensions fall
    back to ``DEFAULT_CATEGORY``.
    """
    return EXTENSION_CATEGORIES.get(extension.lower(), DEFAULT_CATEGORY)
