import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillLayoutTests(unittest.TestCase):
    def test_expected_source_skills_exist(self):
        for name in ("ba", "lead", "plane-ticket-reader", "ticket-workflow"):
            skill = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(skill.is_file(), f"missing source skill: {skill}")

    def test_codex_adapter_points_to_source_skills(self):
        adapter_root = ROOT / "codex" / "agent-ticket-skills" / "skills"
        for name in ("ba", "lead", "plane-ticket-reader", "ticket-workflow"):
            adapter_entry = adapter_root / name
            source_entry = ROOT / "skills" / name
            self.assertTrue(adapter_entry.exists(), f"missing adapter skill: {adapter_entry}")
            self.assertEqual(os.path.realpath(adapter_entry), str(source_entry))


if __name__ == "__main__":
    unittest.main()
