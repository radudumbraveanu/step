---
generated-by: AI, model claude-sonnet-5-5
---

# step

> Early, unstable. Expect breaking changes. The name may change.

View a file, or a folder of files, one step at a time like a wizard. Discuss each step with Claude in the terminal; changes are saved back to the real files.

## Install

Requires Python 3.9+ and internet access (the page loads `marked` and Mermaid from a CDN). Linux and Windows.

Local, per-user install (no pip). From this folder:

```
python install.py            # writes one launcher file: ~/.local/bin/step (Windows: WindowsApps\step.cmd)
python install.py --remove   # deletes that file
```

The launcher points at this folder, so keep the folder where it is, or run the installer again after moving it. The installer never overwrites a `step` it did not write itself (for example the smallstep CLI).

Without installing: run `python -m step_viewer.server [args]` from this folder.

## Start

```
step                    # steps = current directory
step ~/some/dir         # steps = that directory
step -n                 # steps = notes directory ($STEP_NOTES, default ~/notes)
step -n cache-idea      # new note ~/notes/2026-11-21-cache-idea.md, then open it
step -n cache-idea -d   # new note folder ~/notes/2026-11-21-cache-idea/ (index.md + 01-goal.md)
```

It opens your browser on a free port. Options: `-p PORT` to pick the port, `--no-open` to skip the browser. An existing note is opened, never overwritten.

## Read the docs with the tool

The `docs/` folder is a step bundle: each file is a step, in name order (hence the numbers). Run `step docs` from this folder to read it one step at a time: goal, architecture, stack, build plan, usage, demo.

## Warning

`/run` executes any `.py` file under the served folder, and Save overwrites any listed file there, with no sandbox. The server binds to `127.0.0.1` only and refuses requests with another `Host` header. Do not expose it. Do not run `step` in a folder you do not trust.
