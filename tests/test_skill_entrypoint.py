import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ENTRYPOINT = SKILLS / "systematic-research" / "SKILL.md"
SPECIALISTS = (
    "paper-extract",
    "paper-writing",
    "paper-review",
    "paper-plot",
    "analyze-plot",
    "academic-pptx-skill",
)


class SkillEntrypointTests(unittest.TestCase):
    def test_systematic_research_is_the_suite_entrypoint(self):
        text = ENTRYPOINT.read_text(encoding="utf-8")

        self.assertLessEqual(len(text.splitlines()), 100)
        for skill in SPECIALISTS:
            self.assertIn(f"`{skill}`", text)
        self.assertFalse((SKILLS / "paper-orchestrator").exists())
        self.assertTrue(
            (ENTRYPOINT.parent / "references" / "retrieval-workflow.md").is_file()
        )

    def test_entrypoint_frontmatter_keeps_the_canonical_name(self):
        text = ENTRYPOINT.read_text(encoding="utf-8")

        self.assertIn("name: systematic-research", text)
        self.assertIn("description: Use when", text)

    def test_orchestration_and_systematic_search_contracts_are_discoverable(self):
        entrypoint = ENTRYPOINT.read_text(encoding="utf-8")
        orchestration = ENTRYPOINT.parent / "references" / "orchestration-contract.md"
        retrieval = (ENTRYPOINT.parent / "references" / "retrieval-workflow.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("orchestration-contract.md", entrypoint)
        self.assertTrue(orchestration.is_file())
        contract = orchestration.read_text(encoding="utf-8").lower()
        for field in ("artifact id", "produced by", "consumes", "status", "invalidation reason"):
            self.assertIn(field, contract)
        for requirement in ("query log", "inclusion", "exclusion", "stopping condition", "local pdf"):
            self.assertIn(requirement, retrieval.lower())


if __name__ == "__main__":
    unittest.main()
