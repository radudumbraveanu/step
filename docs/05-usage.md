---
generated-by: AI, model claude-sonnet-5-5
---

# Usage

## Situations

| Situation | What to do |
|---|---|
| New idea | `step -n my-idea`, then talk to Claude in a terminal. For a bigger idea use `-d`. |
| Lesson to understand | `cd lesson-dir`, then `step` |
| Build something from zero with AI | `mkdir proj && cd proj`, then `step`, and brainstorm steps there |

## In the viewer

- Pick any `.md`, `.py`, `.html`, `.json` or `.txt` file from the **File** list on the left.
- Two models:
  - **Folder** (entries ending in `/`): each file in the folder is a step. If the folder has an `index.md` (`- [Title](file)` per step, links relative to the index), it sets the order and titles. Without one, files are listed by name.
  - The list shows a folder as one entry (a bundle), not its files. Only files directly in the served directory are listed individually.
  - **Single file** (`.md`): each `## ` section is a step. Other file types are a single step.
- Prev/Next buttons, the step list, or the left/right arrow keys change step. The step number is kept in the URL hash, so a reload stays on the same step.
- `.md` files are rendered. Other files are shown as code, with a Run button for `.py`.
- Edit the files in your own editor, or use the Edit button. The view refreshes within 2 seconds.
- To change something with Claude, run Claude Code in the same directory and quote the step header, for example `2/5 · 02-architecture.md`.
