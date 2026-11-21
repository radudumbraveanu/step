---
generated-by: AI, model claude-sonnet-5-5
---

# Stack

| Piece | Choice | Why |
|-------|--------|-----|
| Page | plain HTML and JS, one file | no build step |
| Markdown | `marked` from CDN | tables, lists, code |
| Diagrams | Mermaid from CDN | matches the repo convention |
| Server | Python stdlib `http.server`, about 130 lines with the CLI | needs to run `.py` and save files, no dependencies |
| Install | `install.py` writes one launcher file, `--remove` deletes it | one `step` command on Linux and Windows, no pip, easy to remove |
| Index | `index.md` (a list of links) | easy for you and Claude to hand-edit, unlike JSON |

Requires Python 3.9+ and internet access for the two CDN scripts.
