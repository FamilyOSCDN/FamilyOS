from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityFindingId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.documentation import DocumentationValidator
from familyos_cli.infrastructure.quality import DocumentationQualityExecutor


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-DOC-001"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-DOC"),
        severity=QualitySeverity.HIGH,
        description="Validate canonical documentation.",
        executor="documentation",
    )


def _executor(*, validator: DocumentationValidator | None = None) -> DocumentationQualityExecutor:
    finding_counter = iter(range(1, 100))
    evidence_counter = iter(range(1, 100))
    return DocumentationQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-{next(finding_counter):04d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-{next(evidence_counter):04d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        monotonic_clock=iter((10.0, 10.25)).__next__,
        validator=validator,
    )


def _target(path: Path | None) -> QualityTarget:
    return QualityTarget(
        target_type="documentation",
        identifier="EPIC-TEST-001",
        revision="abc123",
        path=None if path is None else str(path),
    )


def _write_epic(
    root: Path,
    *,
    deliverables: list[str] | None = None,
    numbered: int = 1,
    canonical_range: str = "00-00",
    controls: int = 1,
) -> None:
    names = deliverables or ["00-EPIC.md", "EPIC.yaml"]
    root.mkdir(parents=True, exist_ok=True)
    import yaml

    payload = {
        "id": "EPIC-TEST-001",
        "deliverables": names,
        "structure": {
            "numbered_documents": numbered,
            "canonical_document_range": canonical_range,
            "control_documents": controls,
            "canonical_files": len(names),
        },
    }
    (root / "EPIC.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")


def _run(executor: DocumentationQualityExecutor, target: QualityTarget):
    return executor.execute(
        check_id=QualityCheckId("QLT-CHECK-DOC-001"),
        rule=_rule(),
        target=target,
    )


def test_valid_documentation_returns_pass_evidence(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# EPIC\n\n## Scope\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1
    evidence = result.evidence[0]
    assert str(evidence.type) == "DOCUMENTATION"
    assert evidence.source == "quality.documentation"
    assert evidence.tool == "familyos-documentation-validator"
    assert evidence.revision == "abc123"
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.metadata == (("violations", "0"),)
    assert result.duration_seconds == 0.25


def test_missing_target_path_returns_error_without_evidence() -> None:
    result = _run(_executor(), _target(None))
    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence == ()
    assert result.diagnostics == ("Documentation quality target.path is required.",)


def test_missing_directory_returns_error_without_evidence(tmp_path: Path) -> None:
    result = _run(_executor(), _target(tmp_path / "missing"))
    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence == ()


def test_missing_required_file_is_fail_finding(tmp_path: Path) -> None:
    _write_epic(tmp_path, deliverables=["00-EPIC.md", "MISSING.md", "EPIC.yaml"], controls=2)

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("MISSING.md" in finding.message for finding in result.findings)
    assert result.evidence[0].result is QualityEvidenceResult.FAIL
    assert all(finding.evidence_ids == ("QLT-EVID-0001",) for finding in result.findings)


def test_empty_required_file_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("is empty" in finding.message for finding in result.findings)


def test_malformed_yaml_is_fail_not_error(tmp_path: Path) -> None:
    (tmp_path / "EPIC.yaml").write_text("structure: [", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    assert "not valid YAML" in result.findings[0].message
    assert result.diagnostics == ()


def test_duplicate_numbered_chapter_is_fail(tmp_path: Path) -> None:
    names = ["00-A.md", "00-B.md", "EPIC.yaml"]
    _write_epic(tmp_path, deliverables=names, numbered=2, canonical_range="00-00")
    (tmp_path / "00-A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "00-B.md").write_text("# B\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("Duplicate numbered chapter 00" in f.message for f in result.findings)


def test_missing_number_from_declared_range_is_fail(tmp_path: Path) -> None:
    names = ["00-A.md", "02-C.md", "EPIC.yaml"]
    _write_epic(tmp_path, deliverables=names, numbered=2, canonical_range="00-02")
    (tmp_path / "00-A.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "02-C.md").write_text("# C\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("Missing numbered chapters" in f.message for f in result.findings)


def test_unclosed_code_fence_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# EPIC\n\n```python\nprint('x')\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("fenced code block is not closed" in f.message for f in result.findings)


def test_multiple_h1_headings_are_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# One\n\n# Two\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("exactly one level-one heading" in f.message for f in result.findings)


def test_skipped_heading_level_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# One\n\n### Three\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("heading level skips" in f.message for f in result.findings)


def test_broken_relative_markdown_reference_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text(
        "# EPIC\n\n[Missing](missing.md)\n",
        encoding="utf-8",
    )

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.FAIL
    assert any("does not resolve" in f.message for f in result.findings)


def test_existing_relative_markdown_reference_passes(tmp_path: Path) -> None:
    names = ["00-EPIC.md", "README.md", "EPIC.yaml"]
    _write_epic(tmp_path, deliverables=names, controls=2)
    (tmp_path / "00-EPIC.md").write_text(
        "# EPIC\n\n[Readme](README.md)\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Readme\n", encoding="utf-8")

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.PASS


def test_external_and_anchor_links_are_not_resolved_locally(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text(
        "# EPIC\n\n[Anchor](#section)\n\n[Web](https://example.com/x)\n",
        encoding="utf-8",
    )

    result = _run(_executor(), _target(tmp_path))

    assert result.status is QualityStatus.PASS

class _FailingDocumentationValidator(DocumentationValidator):
    def __init__(self, exc: Exception) -> None:
        self._exc = exc

    def validate(self, root: Path):
        raise self._exc


def test_control_document_count_mismatch_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path, controls=2)
    (tmp_path / "00-EPIC.md").write_text("# EPIC\n", encoding="utf-8")
    result = _run(_executor(), _target(tmp_path))
    assert result.status is QualityStatus.FAIL
    assert any("Control document count" in f.message for f in result.findings)


def test_canonical_file_count_mismatch_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# EPIC\n", encoding="utf-8")
    epic_yaml = tmp_path / "EPIC.yaml"
    text = epic_yaml.read_text(encoding="utf-8").replace(
        "canonical_files: 2", "canonical_files: 3"
    )
    epic_yaml.write_text(text, encoding="utf-8")
    result = _run(_executor(), _target(tmp_path))
    assert result.status is QualityStatus.FAIL
    assert any("Canonical file count" in f.message for f in result.findings)


def test_invalid_canonical_range_syntax_is_fail(tmp_path: Path) -> None:
    _write_epic(tmp_path, canonical_range="invalid")
    (tmp_path / "00-EPIC.md").write_text("# EPIC\n", encoding="utf-8")
    result = _run(_executor(), _target(tmp_path))
    assert result.status is QualityStatus.FAIL
    assert any("canonical_document_range" in f.message for f in result.findings)


def test_validator_oserror_returns_error_evidence(tmp_path: Path) -> None:
    result = _run(
        _executor(validator=_FailingDocumentationValidator(OSError("read failed"))),
        _target(tmp_path),
    )
    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR


def test_unexpected_validator_failure_returns_error_evidence(tmp_path: Path) -> None:
    result = _run(
        _executor(
            validator=_FailingDocumentationValidator(
                RuntimeError("unexpected validator failure")
            )
        ),
        _target(tmp_path),
    )
    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
