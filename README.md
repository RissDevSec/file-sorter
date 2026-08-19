# 🗂️ file-sorter

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Runtime dependencies](https://img.shields.io/badge/runtime%20dependencies-0-brightgreen.svg)](#-features)

A tiny, dependency-free CLI that tidies a folder by moving files into category
folders based on their extensions. Point it at `~/Downloads`, run one command,
and come back to a clean folder.

## ✨ Features

- 🧹 **Sort by type** — images, documents, videos, music, archives, and more
- 🔠 **Case-insensitive** — `.JPG`, `.Jpg`, and `.jpg` all land in `Images/`
- 🛡️ **No silent overwrites** — duplicate names become `photo (1).jpg`
- 🙈 **Leaves clutter alone** — hidden files, `desktop.ini`, and partial
  downloads (`.crdownload`, `.part`, `.tmp`) are skipped
- 🧯 **Failure-tolerant** — one unreadable file does not stop the whole run
- 📊 **Clear summary** — reports moved, skipped, and failed files
- 🪶 **Zero runtime dependencies** — just the Python standard library
- 🐍 **Python 3.10+**

## 📦 Categories

| Folder      | Extensions                          |
| ----------- | ----------------------------------- |
| `Images`    | `.jpg`, `.jpeg`, `.png`, `.gif`     |
| `Documents` | `.pdf`, `.docx`, `.txt`, `.xlsx`    |
| `Videos`    | `.mp4`, `.mkv`, `.mov`              |
| `Music`     | `.mp3`, `.wav`                      |
| `Archives`  | `.zip`, `.rar`, `.7z`               |
| `Other`     | anything else                       |

> Category names are in English by default. To rename or extend them, edit
> `src/file_sorter/categories.py`.

## 🚀 Installation

### pipx (recommended for CLI tools)

```bash
pipx install git+https://github.com/RissDevSec/file-sorter.git
```

### uv

```bash
uv tool install git+https://github.com/RissDevSec/file-sorter.git
```

### From source

```bash
git clone https://github.com/RissDevSec/file-sorter.git
cd file-sorter
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## 🕹️ Usage

```bash
file-sorter                  # organize ~/Downloads
file-sorter ~/Downloads      # choose a folder explicitly
file-sorter /path/to/folder  # any folder works
file-sorter --help
file-sorter --version
```

### Example

```text
$ file-sorter ~/Downloads
Moved: photo.jpg -> Images/photo.jpg
Moved: report.pdf -> Documents/report.pdf
Moved: backup.zip -> Archives/backup.zip
Skipped: .DS_Store
Done. 3 moved, 1 skipped, 0 failed.
```

If a file with the same name already exists, the new file gets a counter
instead of replacing the old one:

```text
Moved: photo.jpg -> Images/photo (1).jpg
```

### Exit codes

| Code | Meaning                                      |
| ---- | -------------------------------------------- |
| `0`  | Run completed with no failed moves           |
| `1`  | One or more moves failed, or folder not found |
| `2`  | Invalid command-line arguments               |

## 🧠 How it works

1. Read the files directly inside the target folder (subfolders are left alone)
2. Skip directories, hidden files, OS metadata, and partial downloads
3. Match the extension case-insensitively
4. Create the category folder if needed
5. Pick a unique destination name so nothing is overwritten
6. Move the file and print a summary

## 🛡️ Safety notes

- Only top-level files are touched; existing subfolders are not modified
- Hidden files are skipped by default
- Duplicate names are renamed, never overwritten
- A failed move is reported but does not stop the rest of the run
- There is no undo yet — try it on a test folder first if you want to be extra
  careful

## 🗂️ Project structure

```text
file-sorter/
├── src/
│   └── file_sorter/
│       ├── __init__.py       # Package metadata
│       ├── __main__.py       # python -m file_sorter entry point
│       ├── categories.py     # Extension-to-category mapping
│       ├── cli.py            # Argument parsing and output
│       └── organizer.py      # Core move logic
├── tests/
│   ├── test_categories.py
│   ├── test_cli.py
│   └── test_organizer.py
├── pyproject.toml
├── uv.lock
├── README.md
└── LICENSE
```

## 🧑‍💻 Development

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/RissDevSec/file-sorter.git
cd file-sorter
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run the CLI from the checkout:

```bash
uv run file-sorter --help
```

Lint the code:

```bash
uv run --with ruff ruff check .
```

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
