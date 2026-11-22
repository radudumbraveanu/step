---
generated-by: AI, model claude-sonnet-5-5
---

# Build plan

## Built

1. `step_viewer/server.py`: serve, save, run, plus the `step` command (current directory, `-n` notes directory, `-n NAME [-d]` new note, free port, opens the browser, Host check).
2. `step_viewer/viewer.html`: index and single-file section parsing, front matter stripping, Mermaid, poll, edit.
3. `install.py`: local, per-user install of the `step` command (no pip).
4. This proposal as the first test content, plus `06-demo.py`.
5. `tests/test_server.py`: stdlib `unittest`, no dependencies. Covers `new_note` (creates a file or folder, never overwrites) and the server guards (foreign `Host` gets 403, path traversal gets 404, `PUT` only overwrites existing files). Run from the repo root: `python -m unittest discover -s tests -t .`

## Use

See `README.md` for the commands and `05-usage.md` for the viewer.

## Directory browsing

`server.py` serves the chosen directory and lists viewable files at `GET /tree` (hidden folders, `node_modules` and `__pycache__` skipped). The viewer's File list is built from it. To edit an `.md` file itself, use your editor or ask Claude, because picking it shows its steps rather than its text.

## Step sources

- **Folder mode:** pick an entry ending in `/` in the File list. Each file in the folder is one step, shown whole. If the folder has an `index.md`, its `- [Title](file)` links set the order and titles. Otherwise the files are listed by name. `index.md` itself is not listed as a file.
- **Single-file mode:** any other `.md` file is split on `## ` and each section is a step. Text before the first `## ` (usually the `# ` title) is step 1. The Edit button edits only the current section and splices it back into the file on Save.
- **Front matter:** the `generated-by` block at the top of each `.md` file is stripped before rendering, so it never shows in the view.

## Requirements

- Python 3.9+.
- Internet access for the `marked` and Mermaid CDN scripts. It does not work offline.

## Not checked

- `viewer.html` was never opened in a browser. Rendering, Mermaid, polling and the Edit button are untested. Only `server.py` was tested, with curl and the unit tests in `tests/` (the `/run` endpoint, `/tree` and the CLI argument parsing have no unit tests): install into a venv, `step -n` file and `-d` folder creation, `/tree`, `/files`, Host check (403), `-d` without `-n` (error). The browser start (`webbrowser.open`) and Windows were not tested.
- `step` collides with the KDE `step` package (physics simulator) and the smallstep CLI `step` if either is installed.
- Behaviour with very large files or many steps.
