import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANE = ROOT / "skills" / "plane-ticket-reader" / "scripts" / "plane"


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


if __name__ == "__main__":
    unittest.main()
