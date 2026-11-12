#!/usr/bin/env python3
"""Comprueba límites editoriales antes de publicar la guía."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    detail: str


PUBLIC_TEXT_SUFFIXES = {".md", ".tex", ".bib", ".tsv", ".json"}
PUBLIC_ROOT_FILES = {
    "README.md",
    "DISCLAIMER.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
}
SKIPPED_DIRECTORIES = {
    ".git",
    ".superpowers",
    ".worktrees",
    "__pycache__",
    "guia_egel",
    "output",
}
GENERATED_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".synctex.gz",
    ".toc",
    ".xdv",
}


def _walk_files(root: Path) -> list[Path]:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return [root / line for line in result.stdout.splitlines() if line]
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in SKIPPED_DIRECTORIES for part in path.relative_to(root).parts)
    ]


def _tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [root / line for line in result.stdout.splitlines() if line]


def _is_public_text(relative: Path) -> bool:
    if relative.as_posix() in PUBLIC_ROOT_FILES:
        return True
    return (
        relative.suffix.lower() in PUBLIC_TEXT_SUFFIXES
        and relative.parts
        and relative.parts[0] in {"guia", "docs"}
    )


def _text_findings(root: Path, paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    rules = (
        (
            "future-official-edition",
            re.compile(r"edici[oó]n\s+(?:de\s+)?diciembre\s+de\s+2026", re.I),
            "Se atribuye a Ceneval una edición futura no verificable.",
        ),
        (
            "false-endorsement",
            re.compile(
                r"(?:avalad[ao]|aprobad[ao]|certificad[ao]|respaldad[ao])\s+por\s+(?:el\s+)?Ceneval",
                re.I,
            ),
            "El texto sugiere un respaldo oficial de Ceneval.",
        ),
    )
    for path in paths:
        relative = path.relative_to(root)
        if not _is_public_text(relative):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for code, pattern, detail in rules:
            if pattern.search(text):
                findings.append(Finding(code, relative.as_posix(), detail))
    return findings


def _artifact_findings(root: Path, paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        relative = path.relative_to(root)
        name = relative.name
        if name == ".DS_Store":
            findings.append(
                Finding("system-artifact", relative.as_posix(), "Archivo de metadatos de macOS.")
            )
        elif any(name.endswith(suffix) for suffix in GENERATED_SUFFIXES):
            findings.append(
                Finding(
                    "generated-artifact",
                    relative.as_posix(),
                    "Auxiliar de compilación que no debe versionarse.",
                )
            )
    return findings


def _bank_findings(root: Path) -> list[Finding]:
    bank_path = root / "guia" / "datos" / "reactivos.json"
    relative = bank_path.relative_to(root).as_posix()
    if not bank_path.exists():
        return [Finding("missing-bank", relative, "No existe el banco estructurado.")]
    try:
        questions = json.loads(bank_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return [Finding("invalid-bank", relative, f"JSON inválido: {error}")]

    findings: list[Finding] = []
    if not isinstance(questions, list) or len(questions) != 360:
        actual = len(questions) if isinstance(questions, list) else "no es una lista"
        findings.append(
            Finding("question-count", relative, f"Se esperaban 360 reactivos; se encontraron {actual}.")
        )
    if isinstance(questions, list):
        for index, question in enumerate(questions, start=1):
            if not isinstance(question, dict) or not str(question.get("sources", "")).strip():
                identifier = question.get("id", index) if isinstance(question, dict) else index
                findings.append(
                    Finding(
                        "missing-source",
                        relative,
                        f"El reactivo {identifier} no declara una fuente de apoyo.",
                    )
                )
    return findings


def audit_repository(root: Path, *, tracked_only: bool = False) -> list[Finding]:
    root = root.resolve()
    paths = _tracked_files(root) if tracked_only else _walk_files(root)
    return sorted(
        _artifact_findings(root, paths) + _text_findings(root, paths) + _bank_findings(root),
        key=lambda item: (item.path, item.code, item.detail),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Incluye archivos no versionados; por defecto audita únicamente git ls-files.",
    )
    args = parser.parse_args()
    findings = audit_repository(args.root, tracked_only=not args.all_files)
    if findings:
        for finding in findings:
            print(f"{finding.path}: [{finding.code}] {finding.detail}")
        return 1
    print("Auditoría editorial aprobada: banco completo y sin afirmaciones prohibidas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
