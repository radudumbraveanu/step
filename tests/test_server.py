# generated-by: AI, model claude-sonnet-5-5
"""Tests for step_viewer.server. Run from the repo root:

    python -m unittest discover -s tests -t .
"""
import datetime
import http.client
import http.server
import pathlib
import tempfile
import threading
import unittest

from step_viewer import server


class NewNoteTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.notes = pathlib.Path(tmp.name)
        self.today = datetime.date.today().isoformat()

    def test_creates_file_and_never_overwrites(self):
        name = server.new_note(self.notes, "cache idea", as_dir=False)
        self.assertEqual(name, f"{self.today}-cache-idea.md")
        note = self.notes / name
        self.assertTrue(note.read_text(encoding="utf-8").startswith("# Cache idea\n"))

        note.write_text("my own text", encoding="utf-8")
        server.new_note(self.notes, "cache idea", as_dir=False)
        self.assertEqual(note.read_text(encoding="utf-8"), "my own text")

    def test_creates_folder_with_index_and_first_step(self):
        name = server.new_note(self.notes, "Big Idea!", as_dir=True)
        self.assertEqual(name, f"{self.today}-big-idea/")
        folder = self.notes / name
        self.assertEqual((folder / "index.md").read_text(encoding="utf-8"), "- [Goal](01-goal.md)\n")
        self.assertTrue((folder / "01-goal.md").is_file())


class ServerGuardTest(unittest.TestCase):
    """The server must refuse foreign Host headers and anything outside the served folder."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        outer = pathlib.Path(tmp.name).resolve()
        (outer / "secret.txt").write_text("outside", encoding="utf-8")
        root = outer / "steps"
        root.mkdir()
        (root / "01.md").write_text("# inside\n", encoding="utf-8")

        old_root, old_hosts = server.ROOT, set(server.HOSTS)
        server.ROOT = root
        self.addCleanup(setattr, server, "ROOT", old_root)
        self.addCleanup(lambda: (server.HOSTS.clear(), server.HOSTS.update(old_hosts)))

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.port = self.srv.server_address[1]
        server.HOSTS.update({f"127.0.0.1:{self.port}", f"localhost:{self.port}"})
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(self.srv.server_close)
        self.addCleanup(self.srv.shutdown)

    def request(self, method, path, host=None, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        self.addCleanup(conn.close)
        conn.putrequest(method, path, skip_host=True)
        conn.putheader("Host", host or f"127.0.0.1:{self.port}")
        conn.putheader("Content-Length", str(len(body or b"")))
        conn.endheaders(body)
        r = conn.getresponse()
        return r.status, r.read().decode()

    def test_reads_file_inside_folder(self):
        self.assertEqual(self.request("GET", "/files/01.md"), (200, "# inside\n"))

    def test_foreign_host_is_refused(self):
        self.assertEqual(self.request("GET", "/files/01.md", host="evil.example:80")[0], 403)
        self.assertEqual(self.request("PUT", "/files/01.md", host="evil.example:80", body=b"x")[0], 403)

    def test_path_traversal_is_refused(self):
        for path in ("/files/../secret.txt", "/files/%2e%2e/secret.txt"):
            with self.subTest(path=path):
                status, body = self.request("GET", path)
                self.assertEqual(status, 404)
                self.assertNotIn("outside", body)

    def test_put_only_overwrites_existing_files(self):
        self.assertEqual(self.request("PUT", "/files/new.md", body=b"x")[0], 404)
        self.assertEqual(self.request("PUT", "/files/../secret.txt", body=b"x")[0], 404)
        self.assertEqual(self.request("PUT", "/files/01.md", body=b"# changed\n"), (200, "saved"))
        self.assertEqual(self.request("GET", "/files/01.md"), (200, "# changed\n"))


if __name__ == "__main__":
    unittest.main()
