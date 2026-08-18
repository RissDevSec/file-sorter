"""Tests for the command-line interface."""

from pathlib import Path

from file_sorter.cli import build_parser, main


def test_default_folder_is_downloads() -> None:
    args = build_parser().parse_args([])

    assert args.folder == Path.home() / "Downloads"


def test_cli_moves_files_and_prints_a_summary(tmp_path: Path, capsys) -> None:
    (tmp_path / "photo.jpg").write_text("image")
    (tmp_path / ".env").write_text("secret")

    exit_code = main([str(tmp_path)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Moved: photo.jpg -> Images/photo.jpg" in output
    assert "Skipped: .env" in output
    assert "Done. 1 moved, 1 skipped, 0 failed." in output
    assert (tmp_path / "Images" / "photo.jpg").exists()


def test_cli_reports_a_missing_folder(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing"

    exit_code = main([str(missing)])

    assert exit_code == 1
    assert f"Folder not found: {missing}" in capsys.readouterr().out
