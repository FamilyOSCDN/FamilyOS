from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import pytest

from familyos_cli.application.quality import QualityCheckResult
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
from familyos_cli.infrastructure.documentation import (
    DocumentationValidationResult,
    DocumentationValidator,
)
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


def _executor(
    *, validator: DocumentationValidator | None = None,
    repository_epic_roots: tuple[str, ...] | None = None,
) -> DocumentationQualityExecutor:
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
        repository_epic_roots=repository_epic_roots,
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


def _run(
    executor: DocumentationQualityExecutor, target: QualityTarget,
) -> QualityCheckResult:
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

    def validate(self, root: Path) -> DocumentationValidationResult:
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


_REPOSITORY_ROOTS = ("docs/epics/EPIC-B", "docs/epics/EPIC-A")


@pytest.mark.parametrize("has_violations", [False, True])
def test_repository_scope_normalizes_one_correlated_result(
    tmp_path: Path, has_violations: bool,
) -> None:
    for relative in _REPOSITORY_ROOTS:
        epic = tmp_path / relative
        _write_epic(epic)
        (epic / "00-EPIC.md").write_text(
            "No heading\n" if has_violations else "# Valid EPIC\n",
            encoding="utf-8",
        )
    target = replace(_target(tmp_path), target_type="repository")

    result = _run(_executor(repository_epic_roots=_REPOSITORY_ROOTS), target)

    expected_count = 2 if has_violations else 0
    assert result.status is (QualityStatus.FAIL if has_violations else QualityStatus.PASS)
    assert result.diagnostics == ()
    assert len(result.evidence) == 1
    assert len(result.findings) == expected_count
    evidence = result.evidence[0]
    assert evidence.result is (
        QualityEvidenceResult.FAIL if has_violations else QualityEvidenceResult.PASS
    )
    assert evidence.target is target
    assert evidence.revision == target.revision
    assert evidence.rule_id == _rule().id
    assert evidence.source == "quality.documentation"
    assert evidence.tool == "familyos-documentation-validator"
    assert evidence.type.value == "DOCUMENTATION"
    assert evidence.metadata == (
        ("violations", str(expected_count)),
        ("scope", "repository_epics"),
        ("epic_roots", "\n".join(_REPOSITORY_ROOTS)),
    )
    if has_violations:
        assert [f.location for f in result.findings] == [
            f"{relative}/00-EPIC.md" for relative in _REPOSITORY_ROOTS
        ]
        assert len({f.id for f in result.findings}) == 2
        assert all(f.target is target for f in result.findings)
        assert all(f.rule_id == _rule().id for f in result.findings)
        assert all(f.domain == _rule().domain for f in result.findings)
        assert all(f.severity == _rule().severity for f in result.findings)
        assert all(f.evidence_ids == (str(evidence.id),) for f in result.findings)


@pytest.mark.parametrize("target_type", ["documentation", "plugin"])
def test_configured_scope_does_not_change_other_target_types(
    tmp_path: Path, target_type: str,
) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# Valid EPIC\n", encoding="utf-8")
    target = replace(_target(tmp_path), target_type=target_type)

    result = _run(_executor(repository_epic_roots=_REPOSITORY_ROOTS), target)

    assert result.status is QualityStatus.PASS
    assert result.evidence[0].metadata == (("violations", "0"),)


def test_unconfigured_repository_target_keeps_direct_epic_behavior(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# Valid EPIC\n", encoding="utf-8")

    result = _run(_executor(), replace(_target(tmp_path), target_type="repository"))

    assert result.status is QualityStatus.PASS
    assert result.evidence[0].metadata == (("violations", "0"),)


def test_repository_scope_does_not_fall_back_to_valid_root_manifest(tmp_path: Path) -> None:
    _write_epic(tmp_path)
    (tmp_path / "00-EPIC.md").write_text("# Valid root EPIC\n", encoding="utf-8")
    target = replace(_target(tmp_path), target_type="repository")

    result = _run(_executor(repository_epic_roots=_REPOSITORY_ROOTS), target)

    assert result.status is QualityStatus.FAIL
    assert [f.location for f in result.findings] == [
        f"{relative}/EPIC.yaml" for relative in _REPOSITORY_ROOTS
    ]
    assert result.evidence[0].metadata[0] == ("violations", "2")


@pytest.mark.parametrize("error", [PermissionError, OSError, RuntimeError])
def test_repository_execution_error_retains_configured_scope_evidence(
    tmp_path: Path, error: type[Exception],
) -> None:
    target = replace(_target(tmp_path), target_type="repository")
    result = _run(
        _executor(
            validator=_FailingDocumentationValidator(error("selected EPIC unreadable")),
            repository_epic_roots=_REPOSITORY_ROOTS,
        ),
        target,
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.diagnostics == (
        "Documentation validation could not complete: selected EPIC unreadable",
    )
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert result.evidence[0].target is target
    assert result.evidence[0].metadata == (
        ("violations", "0"),
        ("scope", "repository_epics"),
        ("epic_roots", "\n".join(_REPOSITORY_ROOTS)),
    )


def test_escaping_repository_root_produces_error_evidence(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    selected = repository / _REPOSITORY_ROOTS[0]
    selected.parent.mkdir(parents=True)
    outside = tmp_path / "outside"
    _write_epic(outside)
    selected.symlink_to(outside, target_is_directory=True)

    result = _run(
        _executor(repository_epic_roots=_REPOSITORY_ROOTS),
        replace(_target(repository), target_type="repository"),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert "outside the target" in result.diagnostics[0]
    assert ("epic_roots", "\n".join(_REPOSITORY_ROOTS)) in result.evidence[0].metadata


@pytest.mark.parametrize("scope", [(), [], (42,), ("docs/epics/EPIC-A", "docs/epics/EPIC-A")])
def test_invalid_scope_is_rejected_at_composition(scope: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        _executor(repository_epic_roots=cast(tuple[str, ...], scope))


def test_missing_repository_target_does_not_claim_execution_evidence(tmp_path: Path) -> None:
    result = _run(
        _executor(repository_epic_roots=_REPOSITORY_ROOTS),
        replace(_target(tmp_path / "missing"), target_type="repository"),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence == ()
