import contextlib
import importlib.machinery
import importlib.util
import io
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANE = ROOT / "skills" / "plane-ticket-reader" / "scripts" / "plane"


def load_plane_module():
    loader = importlib.machinery.SourceFileLoader("plane_cli", str(PLANE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def run_plane(*args):
    return subprocess.run(
        ["python3", str(PLANE), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class PlaneCliTests(unittest.TestCase):
    def test_help_runs_without_credentials(self):
        result = run_plane("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Plane.so read-only CLI", result.stdout)
        self.assertIn("projects", result.stdout)
        self.assertIn("issues", result.stdout)

    def test_issue_help_exposes_only_read_commands(self):
        result = run_plane("issues", "--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("list", result.stdout)
        self.assertIn("get", result.stdout)
        self.assertIn("fast-get", result.stdout)
        self.assertIn("search", result.stdout)
        self.assertNotIn("create", result.stdout)
        self.assertNotIn("update", result.stdout)
        self.assertNotIn("delete", result.stdout)
        self.assertNotIn("assign", result.stdout)

    def test_comments_help_exposes_only_list(self):
        result = run_plane("comments", "--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("list", result.stdout)
        self.assertNotIn("add", result.stdout)

    def test_split_ticket_id_normalizes_project_key(self):
        plane = load_plane_module()

        self.assertEqual(plane.split_ticket_id("tad-1816"), ("TAD", 1816))

    def test_split_ticket_id_rejects_invalid_shapes(self):
        plane = load_plane_module()

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            plane.split_ticket_id("TAD")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            plane.split_ticket_id("TAD-abc")

    def test_validate_id_rejects_path_characters(self):
        plane = load_plane_module()

        self.assertEqual(plane.validate_id("project-uuid", "project ID"), "project-uuid")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            plane.validate_id("../secret", "project ID")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            plane.validate_id("folder/name", "project ID")

    def test_paged_get_follows_next_links(self):
        plane = load_plane_module()
        calls = []

        def fake_api_get(endpoint):
            calls.append(endpoint)
            if endpoint == "/first":
                return {
                    "results": [{"id": "one"}],
                    "next": "https://plane.example.com/api/v1/second",
                }
            if endpoint == "/second":
                return {"results": [{"id": "two"}], "next": None}
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        original_api_get = plane.api_get
        plane.api_get = fake_api_get
        try:
            self.assertEqual(plane.paged_get("/first"), [{"id": "one"}, {"id": "two"}])
        finally:
            plane.api_get = original_api_get

        self.assertEqual(calls, ["/first", "/second"])


if __name__ == "__main__":
    unittest.main()
