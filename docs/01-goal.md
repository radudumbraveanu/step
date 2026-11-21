---
generated-by: AI, model claude-sonnet-5-5
---

# Goal

Think about a problem in wizard-like steps: view a file (or a folder of files) one step at a time, discuss each step with Claude in the terminal, and have every change saved back to the real files.

## In scope

- Browse and edit any `.md`, `.py`, `.html`, `.json` or `.txt` file under the repo root, picked from a File list.
- One step at a time, with Prev/Next and a step list.
- Two models: a single `.md` file (each `## ` section is a step), or a folder (each file is a step, optionally ordered by an `index.md`).
- `.md` steps are rendered (tables, lists, Mermaid). `.py` steps show the code plus a Run button.
- The view refreshes by itself when a file changes.

## Out of scope

- A chat box inside the page (chat happens in Claude Code).
- Multi-user, auth, sandboxing, build step.
