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

    def test_ticket_workflow_uses_ticket_scoped_artifacts(self):
        workflow = (ROOT / "skills" / "ticket-workflow" / "SKILL.md").read_text(encoding="utf-8")
        lifecycle = (
            ROOT / "skills" / "ticket-workflow" / "references" / "ticket-lifecycle.md"
        ).read_text(encoding="utf-8")
        combined = workflow + "\n" + lifecycle

        for expected in (
            "tasks/<ticket-id>/ticket-context.json",
            "tasks/<ticket-id>/spec.md",
            "tasks/<ticket-id>/plan.md",
            "tasks/<ticket-id>/adr.md",
            "findings.md",
            "progress.md",
        ):
            self.assertIn(expected, combined)

        self.assertNotIn("specs/FEAT-XXX", combined)
        self.assertNotIn("docs/adr/NNNN", combined)


if __name__ == "__main__":
    unittest.main()
