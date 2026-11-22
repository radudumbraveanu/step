---
generated-by: AI, model claude-sonnet-5-5
---

# step

> Early, unstable. Expect breaking changes. The name may change.

View a file, or a folder of files, one step at a time like a wizard. Discuss each step with Claude in the terminal; changes are saved back to the real files.

## Why steps

The idea of this app comes from a few well-known principles of teaching and learning: teach in small pieces, sized so the learner can absorb them, going from simple to complex. `step` is a tool to apply them to your own notes, lessons and ideas.

| Principle | In `step` |
|---|---|
| [Cognitive load](https://en.wikipedia.org/wiki/Cognitive_load): working memory is small, too much at once means nothing is retained | One step on screen at a time. Tables, diagrams and short examples instead of long prose. |
| [Chunking](https://en.wikipedia.org/wiki/Chunking_%28psychology%29): split material into small units | One `## ` section, or one file in a folder, is one step. |
| [Progressive disclosure](https://en.wikipedia.org/wiki/Progressive_disclosure): show only what is needed now, the rest on request | Prev/Next and the step list. Later steps stay out of sight until you reach them. |
| [Zone of proximal development](https://en.wikipedia.org/wiki/Zone_of_proximal_development): not too easy, not too hard | You set the pace. Stay on a step, go back, or ask Claude to explain it differently. |
| [Instructional scaffolding](https://en.wikipedia.org/wiki/Instructional_scaffolding): support while learning, then less | Claude in the terminal answers about the current step (quote its header). Ask for less help as you get comfortable. |
| [Programmed instruction](https://en.wikipedia.org/wiki/Programmed_instruction): small steps with immediate feedback | An edit shows in the viewer within 2 seconds. The Run button on a `.py` step runs the code at once. |

Order the steps from simple to complex: each step should use only what earlier steps introduced.

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
