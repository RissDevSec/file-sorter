"""Tests for the extension-to-category mapping."""

import pytest

from file_sorter.categories import DEFAULT_CATEGORY, FILE_CATEGORIES, categorize


@pytest.mark.parametrize(
    ("extension", "expected"),
    [
        (".jpg", "Images"),
        (".JPG", "Images"),
        (".pdf", "Documents"),
        (".mp4", "Videos"),
        (".mp3", "Music"),
        (".zip", "Archives"),
        (".unknown", DEFAULT_CATEGORY),
        ("", DEFAULT_CATEGORY),
    ],
)
def test_categorize(extension: str, expected: str) -> None:
    assert categorize(extension) == expected


def test_every_configured_extension_is_mapped() -> None:
    for category, extensions in FILE_CATEGORIES.items():
        for extension in extensions:
            assert categorize(extension) == category
