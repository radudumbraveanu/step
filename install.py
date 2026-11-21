# generated-by: AI, model claude-sonnet-5-5
"""Local, per-user install of the `step` command. No pip, no packaging.

    python install.py            install
    python install.py --remove   remove

It writes ONE small launcher file that points at this folder:
    Linux/macOS: ~/.local/bin/step
    Windows:     %LOCALAPPDATA%\\Microsoft\\WindowsApps\\step.cmd   (already on PATH)
If you move or delete this folder, the command stops working: run the installer again.
It never touches a `step` file that it did not write itself (for example the smallstep CLI).
"""
import os
import pathlib
import shlex
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent
WIN = os.name == "nt"
if WIN:
    LOCAL = pathlib.Path(os.environ.get("LOCALAPPDATA") or pathlib.Path.home() / "AppData" / "Local")
    BIN = LOCAL / "Microsoft" / "WindowsApps"
else:
    BIN = pathlib.Path.home() / ".local" / "bin"
TARGET = BIN / ("step.cmd" if WIN else "step")
MARK = "written by install.py"  # how we recognise our own launcher


def launcher():
    if WIN:
        return (
            "@echo off\n"
            f"REM generated-by: AI, model claude-sonnet-5-5; {MARK}; remove with: python install.py --remove\n"
            "setlocal\n"
            f'set "PYTHONPATH={REPO}"\n'
            "python -m step_viewer.server %*\n"
        )
    return (
        "#!/bin/sh\n"
        f"# generated-by: AI, model claude-sonnet-5-5; {MARK}; remove with: python install.py --remove\n"
        f'PYTHONPATH={shlex.quote(str(REPO))}"${{PYTHONPATH:+:$PYTHONPATH}}" exec python3 -m step_viewer.server "$@"\n'
    )


def ours(path):
    try:
        return MARK in path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


def remove():
    if not TARGET.exists():
        return print(f"nothing to remove: {TARGET}")
    if not ours(TARGET):
        sys.exit(f"{TARGET} was not written by install.py, so I leave it alone. Remove it yourself if you want.")
    TARGET.unlink()
    print(f"removed {TARGET}")


def install():
    if TARGET.exists() and not ours(TARGET):
        sys.exit(f"{TARGET} exists and was not written by install.py (another `step` tool?). Not overwriting it.")
    BIN.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(launcher(), encoding="utf-8")
    if not WIN:
        TARGET.chmod(0o755)
    print(f"installed {TARGET}\npoints at   {REPO}")
    if str(BIN) not in os.environ.get("PATH", "").split(os.pathsep):
        print(f"\nNOTE: {BIN} is not on your PATH. Add it, then open a new terminal.")
    found = shutil.which("step")
    if found and pathlib.Path(found).resolve() != TARGET.resolve():
        print(f"\nNOTE: `step` currently resolves to {found}, which comes first on your PATH.")
    print("\ntry:  step --help      remove:  python install.py --remove")


if sys.version_info < (3, 9):
    sys.exit("Python 3.9+ is required")
args = sys.argv[1:]
if args == ["--remove"]:
    remove()
elif not args:
    install()
else:
    sys.exit("usage: python install.py [--remove]")
