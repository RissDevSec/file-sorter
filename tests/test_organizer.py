"""Tests for the core file organization logic."""

import shutil
from pathlib import Path

from file_sorter.organizer import organize, unique_destination


def test_organize_moves_files_into_category_folders(tmp_path: Path) -> None:
    (tmp_path / "photo.JPG").write_text("image")
    (tmp_path / "report.pdf").write_text("doc")
    (tmp_path / "archive.zip").write_text("zip")
    (tmp_path / "notes").write_text("plain")

    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "keep.txt").write_text("keep")

    result = organize(tmp_path)

    assert sorted(
        (source.name, destination.parent.name)
        for source, destination in result.moved
    ) == [
        ("archive.zip", "Archives"),
        ("notes", "Other"),
        ("photo.JPG", "Images"),
        ("report.pdf", "Documents"),
    ]
    assert (tmp_path / "Images" / "photo.JPG").read_text() == "image"
    assert (tmp_path / "Documents" / "report.pdf").read_text() == "doc"
    assert (tmp_path / "Archives" / "archive.zip").read_text() == "zip"
    assert (tmp_path / "Other" / "notes").read_text() == "plain"
    assert (nested / "keep.txt").exists()


def test_duplicate_names_are_renamed(tmp_path: Path) -> None:
    target = tmp_path / "Images"
    target.mkdir()
    (target / "photo.jpg").write_text("existing")
    (tmp_path / "photo.jpg").write_text("new")

    result = organize(tmp_path)

    assert (target / "photo.jpg").read_text() == "existing"
    assert (target / "photo (1).jpg").read_text() == "new"
    assert len(result.moved) == 1


def test_unique_destination_adds_a_counter(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").write_text("existing")

    destination = unique_destination(tmp_path, "photo.jpg")

    assert destination == tmp_path / "photo (1).jpg"


def test_hidden_and_incomplete_files_are_skipped(tmp_path: Path) -> None:
    ignored_files = [
        ".env",
        ".DS_Store",
        "desktop.ini",
        "movie.mp4.crdownload",
        "document.pdf.part",
        "keep.tmp",
    ]
    for filename in ignored_files:
        (tmp_path / filename).write_text("ignored")

    result = organize(tmp_path)

    assert result.moved == []
    assert {path.name for path in result.skipped} == set(ignored_files)
    for filename in ignored_files:
        assert (tmp_path / filename).exists()


def test_failed_move_is_recorded_and_other_files_continue(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "broken.pdf").write_text("broken")
    (tmp_path / "ok.pdf").write_text("ok")

    real_move = shutil.move

    def fake_move(source: Path, destination: Path) -> None:
        if Path(source).name == "broken.pdf":
            raise OSError("permission denied")
        real_move(source, destination)

    monkeypatch.setattr("file_sorter.organizer.shutil.move", fake_move)

    result = organize(tmp_path)

    assert [source.name for source, _ in result.failed] == ["broken.pdf"]
    assert [source.name for source, _ in result.moved] == ["ok.pdf"]
    assert (tmp_path / "broken.pdf").exists()
    assert (tmp_path / "Documents" / "ok.pdf").exists()
