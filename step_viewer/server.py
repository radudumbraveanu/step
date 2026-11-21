# generated-by: AI, model claude-sonnet-5-5
"""step: view a folder or a markdown file one step at a time, in the browser.

    step                    steps = current directory
    step DIR                steps = DIR
    step -n                 steps = notes directory ($STEP_NOTES, default ~/notes)
    step -n NAME            new note file  <notes>/<date>-<name>.md, then open it
    step -n NAME -d         new note dir   <notes>/<date>-<name>/ (index.md + 01-goal.md), then open it
    options: -p PORT (default: any free port), --no-open (do not start the browser)

GET  /               viewer.html
GET  /tree           newline-separated list of viewable files under the folder
GET  /files/<name>   read a file under the folder
PUT  /files/<name>   overwrite an EXISTING file under the folder
GET  /run?file=x.py  run a .py file under the folder, return stdout+stderr
shortcut: runs any .py and overwrites any listed file under the folder, no sandbox.
Bound to 127.0.0.1 and requests with another Host header are refused; never expose it.
"""
import argparse
import datetime
import http.server
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import webbrowser

HERE = pathlib.Path(__file__).parent.resolve()
SKIP = {"node_modules", "__pycache__", "venv", "target", "build", "dist"}
EXTS = {".md", ".py", ".html", ".json", ".txt"}
ROOT = pathlib.Path.cwd()  # set in main()
HOSTS = set()  # allowed Host header values, set in main()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):  # the page polls every 2s; keep the terminal quiet
        pass

    def reply(self, code, body, ctype="text/plain; charset=utf-8"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def target(self, name):
        p = (ROOT / urllib.parse.unquote(name)).resolve()
        return p if p.is_relative_to(ROOT) and p.is_file() else None

    def do_GET(self):
        if self.headers.get("Host") not in HOSTS:  # blocks DNS rebinding
            return self.reply(403, "bad host")
        u = urllib.parse.urlparse(self.path)
        if u.path == "/":
            return self.reply(200, (HERE / "viewer.html").read_bytes(), "text/html; charset=utf-8")
        if u.path == "/tree":
            files = sorted(
                p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                if p.is_file() and p.suffix in EXTS
                and not any(s.startswith(".") or s in SKIP for s in p.relative_to(ROOT).parts)
            )
            return self.reply(200, "\n".join(files))
        if u.path.startswith("/files/"):
            p = self.target(u.path[len("/files/"):])
            return self.reply(200, p.read_bytes()) if p else self.reply(404, "not found")
        if u.path == "/run":
            name = urllib.parse.parse_qs(u.query).get("file", [""])[0]
            p = self.target(name)
            if not p or p.suffix != ".py":
                return self.reply(404, "not a .py file in the steps folder")
            try:
                r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, timeout=10, cwd=p.parent)
                return self.reply(200, r.stdout + r.stderr)
            except subprocess.TimeoutExpired:
                return self.reply(200, "timeout after 10s")
        self.reply(404, "not found")

    def do_PUT(self):
        if self.headers.get("Host") not in HOSTS:
            return self.reply(403, "bad host")
        if not self.path.startswith("/files/"):
            return self.reply(404, "not found")
        p = self.target(self.path[len("/files/"):])
        if not p:
            return self.reply(404, "not found (only existing files can be saved)")
        p.write_bytes(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        self.reply(200, "saved")


def new_note(notes, name, as_dir):
    """Create <date>-<name>.md (or a folder) in notes unless it exists. Returns the path relative to notes."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "note"
    title = re.sub(r"[-_]+", " ", name).strip()
    title = title[:1].upper() + title[1:]
    base = f"{datetime.date.today().isoformat()}-{slug}"
    if as_dir:
        d = notes / base
        if not d.exists():
            d.mkdir(parents=True)
            (d / "index.md").write_text("- [Goal](01-goal.md)\n", encoding="utf-8")
            (d / "01-goal.md").write_text(f"# {title}\n\n## Goal\n\nWhat is this about? Write it here, or ask Claude.\n", encoding="utf-8")
        return base + "/"
    f = notes / (base + ".md")
    if not f.exists():
        f.write_text(f"# {title}\n\n## Idea\n\nWhat is this about? Write it here, or ask Claude.\n", encoding="utf-8")
    return f.name


def main():
    global ROOT
    ap = argparse.ArgumentParser(prog="step", description="View a folder or a markdown file one step at a time.")
    ap.add_argument("dir", nargs="?", help="folder to view (default: current directory)")
    ap.add_argument("-n", "--notes", nargs="?", const="", metavar="NAME",
                    help="use the notes directory; with NAME, create that note first")
    ap.add_argument("-d", "--dir-note", action="store_true", help="with -n NAME: create a folder instead of a file")
    ap.add_argument("-p", "--port", type=int, default=0, help="port (default: any free port)")
    ap.add_argument("--no-open", action="store_true", help="do not open the browser")
    a = ap.parse_args()
    if a.dir_note and not a.notes:
        ap.error("-d needs -n NAME")

    if a.dir:
        ROOT = pathlib.Path(a.dir)
    elif a.notes is not None:
        ROOT = pathlib.Path(os.environ.get("STEP_NOTES") or pathlib.Path.home() / "notes")
    if a.notes is not None:
        ROOT.mkdir(parents=True, exist_ok=True)
    ROOT = ROOT.resolve()
    if not ROOT.is_dir():
        ap.error(f"not a folder: {ROOT}")

    start = new_note(ROOT, a.notes, a.dir_note) if a.notes else ""
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    port = srv.server_address[1]
    HOSTS.update({f"127.0.0.1:{port}", f"localhost:{port}"})
    url = f"http://127.0.0.1:{port}/" + (f"#src={urllib.parse.quote(start, safe='')}&i=0" if start else "")
    print(f"steps: {ROOT}\nopen:  {url}\nCtrl+C to stop", flush=True)
    if not a.no_open:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
