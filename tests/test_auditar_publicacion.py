import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.auditar_publicacion import audit_repository


class AuditRepositoryTests(unittest.TestCase):
    def make_repository(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "guia" / "datos").mkdir(parents=True)
        questions = [
            {
                "id": f"H-{number:03d}",
                "stem": f"Pregunta original número {number} con contexto suficiente",
                "options": ["Correcta", "Distractor uno", "Distractor dos"],
                "reasons": ["Razón", "Explicación uno", "Explicación dos"],
                "sources": "fuente",
            }
            for number in range(1, 361)
        ]
        (root / "guia" / "datos" / "reactivos.json").write_text(
            json.dumps(questions), encoding="utf-8"
        )
        (root / "README.md").write_text(
            "Material independiente y no oficial.", encoding="utf-8"
        )
        return root

    def test_accepts_original_bank_with_360_sourced_questions(self):
        root = self.make_repository()

        findings = audit_repository(root)

        self.assertEqual([], findings)

    def test_rejects_future_ceneval_edition_claim(self):
        root = self.make_repository()
        (root / "README.md").write_text(
            "Basada en la guía oficial, edición de diciembre de 2026.",
            encoding="utf-8",
        )

        findings = audit_repository(root)

        self.assertTrue(any(item.code == "future-official-edition" for item in findings))

    def test_rejects_claim_of_ceneval_endorsement(self):
        root = self.make_repository()
        (root / "README.md").write_text(
            "Esta guía está avalada por Ceneval.", encoding="utf-8"
        )

        findings = audit_repository(root)

        self.assertTrue(any(item.code == "false-endorsement" for item in findings))

    def test_rejects_unsourced_or_wrong_sized_bank(self):
        root = self.make_repository()
        questions = json.loads(
            (root / "guia" / "datos" / "reactivos.json").read_text(encoding="utf-8")
        )
        questions.pop()
        questions[0]["sources"] = ""
        (root / "guia" / "datos" / "reactivos.json").write_text(
            json.dumps(questions), encoding="utf-8"
        )

        findings = audit_repository(root)

        codes = {item.code for item in findings}
        self.assertIn("question-count", codes)
        self.assertIn("missing-source", codes)

    def test_rejects_forbidden_generated_artifacts(self):
        root = self.make_repository()
        (root / "guia" / "main.aux").write_text("aux", encoding="utf-8")
        (root / ".DS_Store").write_text("metadata", encoding="utf-8")

        findings = audit_repository(root)

        codes = {item.code for item in findings}
        self.assertIn("generated-artifact", codes)
        self.assertIn("system-artifact", codes)

    def test_all_files_mode_respects_gitignore(self):
        root = self.make_repository()
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        (root / ".gitignore").write_text(".DS_Store\n", encoding="utf-8")
        (root / ".DS_Store").write_text("metadata", encoding="utf-8")

        findings = audit_repository(root)

        self.assertFalse(any(item.code == "system-artifact" for item in findings))


if __name__ == "__main__":
    unittest.main()
