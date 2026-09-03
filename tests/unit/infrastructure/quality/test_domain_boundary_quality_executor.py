import tokenize
from datetime import UTC, datetime
from pathlib import Path
from typing import Never

import pytest

from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.application.quality.domain_boundary_quality_policy import (
    ARCHITECTURE_CHECK_ID,
    DOMAIN_BOUNDARY_RULE,
    DOMAIN_SOURCE_ROOT,
)
from familyos_cli.domain.quality import (
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityFindingId,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.quality.domain_boundary_quality_executor import (
    DomainBoundaryQualityExecutor,
)


def _execute(
    root: Path, *, target_type: str = "repository", path: bool = True
) -> QualityCheckResult:
    counter = iter(range(100))
    return DomainBoundaryQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(f"QLT-FIND-ARC-{next(counter)}"),
        evidence_id_factory=lambda: QualityEvidenceId("QLT-EVID-ARC-1"),
        clock=lambda: datetime(2026, 9, 3, tzinfo=UTC),
        monotonic_clock=iter((2.0, 2.25)).__next__,
    ).execute(
        check_id=ARCHITECTURE_CHECK_ID,
        rule=DOMAIN_BOUNDARY_RULE,
        target=QualityTarget(
            target_type,
            "fixture",
            revision="checked-revision",
            path=str(root) if path else None,
        ),
    )


def _source(root: Path, text: str, name: str = "example.py") -> Path:
    path = root / DOMAIN_SOURCE_ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "source",
    [
        "import familyos_cli.infrastructure.db",
        "import familyos_cli.application as app",
        "from familyos_cli.interfaces import cli",
        "from familyos_cli import infrastructure",
        "from ..infrastructure import db",
        "from .. import application",
        "if False:\n    from familyos_cli import interfaces",
        "def example():\n    import familyos_cli.infrastructure",
        "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    import familyos_cli.application",
    ],
)
def test_forbidden_import_forms_produce_canonical_findings(
    tmp_path: Path, source: str
) -> None:
    _source(tmp_path, source)
    result = _execute(tmp_path)
    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    finding = result.findings[0]
    evidence = result.evidence[0]
    assert finding.rule_id == DOMAIN_BOUNDARY_RULE.id
    assert finding.domain == DOMAIN_BOUNDARY_RULE.domain
    assert finding.severity == DOMAIN_BOUNDARY_RULE.severity
    assert finding.target is evidence.target
    assert finding.evidence_ids == (str(evidence.id),)
    assert finding.location is not None and finding.location.startswith(
        DOMAIN_SOURCE_ROOT
    )
    assert "forbidden outer-layer module" in finding.message
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.type.value == "ARCHITECTURE"
    assert evidence.revision == "checked-revision"
    assert evidence.rule_id == finding.rule_id
    assert evidence.requirement_id == DOMAIN_BOUNDARY_RULE.requirement_id
    assert evidence.source == "quality.architecture"
    assert evidence.tool == "python.ast" and evidence.tool_version
    assert ("inspected_files", "1") in evidence.metadata
    assert ("violations", "1") in evidence.metadata
    assert result.duration_seconds == 0.25


@pytest.mark.parametrize(
    "name",
    [
        "nested/__init__.py",
        "nested/__init__.pyi",
        "nested/example.py",
        "nested/example.pyi",
    ],
)
def test_nested_relative_imports_use_containing_package(
    tmp_path: Path, name: str
) -> None:
    _source(tmp_path, "from ... import infrastructure", name)
    result = _execute(tmp_path)
    assert result.status is QualityStatus.FAIL
    assert result.findings[0].message.endswith("familyos_cli.infrastructure")
    assert result.findings[0].location == f"{DOMAIN_SOURCE_ROOT}/{name}:1:1"


@pytest.mark.parametrize(
    "source",
    [
        "from dataclasses import dataclass\nfrom familyos_cli.domain import family",
        "from .. import domain",
        "import familyos_cli.infrastructure_extra",
        "from familyos_cli import application_extra",
        "# import familyos_cli.infrastructure\ntext = 'from familyos_cli import application'",
        "raise RuntimeError('must not execute source')",
    ],
)
def test_compliant_source_is_pass_and_is_never_executed(
    tmp_path: Path, source: str
) -> None:
    _source(tmp_path, source)
    result = _execute(tmp_path)
    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert result.diagnostics == ()
    assert result.evidence[0].result is QualityEvidenceResult.PASS


def test_deterministic_order_and_distinct_import_statements(tmp_path: Path) -> None:
    _source(
        tmp_path,
        "from familyos_cli.infrastructure import A, B\nimport familyos_cli.interfaces",
        "z.py",
    )
    _source(
        tmp_path,
        "import familyos_cli.interfaces, familyos_cli.application\nimport familyos_cli.interfaces",
        "a.py",
    )
    result = _execute(tmp_path)
    assert [finding.location for finding in result.findings] == [
        f"{DOMAIN_SOURCE_ROOT}/a.py:1:1",
        f"{DOMAIN_SOURCE_ROOT}/a.py:1:1",
        f"{DOMAIN_SOURCE_ROOT}/a.py:2:1",
        f"{DOMAIN_SOURCE_ROOT}/z.py:1:1",
        f"{DOMAIN_SOURCE_ROOT}/z.py:2:1",
    ]
    assert result.findings[0].message.endswith("familyos_cli.application")
    assert result.findings[1].message.endswith("familyos_cli.interfaces")
    assert len({finding.id for finding in result.findings}) == 5
    assert ("inspected_files", "2") in result.evidence[0].metadata


def test_ast_column_is_one_based_and_non_utf8_source_is_supported(
    tmp_path: Path,
) -> None:
    file = _source(tmp_path, "")
    file.write_bytes(
        b"# coding: latin-1\n# caf\xe9\nif False:\n    import familyos_cli.infrastructure\n"
    )
    result = _execute(tmp_path)
    assert result.status is QualityStatus.FAIL
    assert result.findings[0].location == f"{DOMAIN_SOURCE_ROOT}/example.py:4:5"


@pytest.mark.parametrize(
    "case",
    ["missing", "empty", "syntax", "encoding", "relative", "wrong-target", "no-path"],
)
def test_unreliable_scan_is_error_without_partial_findings(
    tmp_path: Path, case: str
) -> None:
    if case != "missing":
        source = _source(tmp_path, "import familyos_cli.infrastructure", "a.py")
        if case == "empty":
            source.unlink()
        if case == "syntax":
            _source(tmp_path, "def invalid(", "z.py")
        if case == "encoding":
            _source(tmp_path, "", "z.py").write_bytes(b"\xff")
        if case == "relative":
            _source(tmp_path, "from ... import outside", "z.py")
    result = _execute(
        tmp_path,
        target_type="plugin" if case == "wrong-target" else "repository",
        path=case != "no-path",
    )
    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", "architecture_scan_failed") in result.evidence[0].metadata
    assert not any(
        key in ("inspected_files", "violations")
        for key, _ in result.evidence[0].metadata
    )
    assert result.diagnostics[0].startswith("Architecture scan failed:")


@pytest.mark.parametrize("kind", ["file", "directory", "root", "broken"])
def test_symbolic_links_never_skip_or_expand_scan_scope(
    tmp_path: Path, kind: str
) -> None:
    repository = tmp_path / "repository"
    _source(repository, "pass")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "bad.py").write_text("import familyos_cli.infrastructure")
    root = repository / DOMAIN_SOURCE_ROOT
    if kind == "root":
        moved = root.with_name("moved")
        root.rename(moved)
        root.symlink_to(moved, target_is_directory=True)
    else:
        target = (
            outside
            if kind == "directory"
            else outside / ("bad.py" if kind == "file" else "absent.py")
        )
        (root / "link").symlink_to(target, target_is_directory=kind == "directory")
    result = _execute(repository)
    assert result.status is QualityStatus.ERROR
    assert "symbolic link" in result.diagnostics[0]


def test_unreadable_source_is_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _source(tmp_path, "pass")

    def denied(path: Path) -> Never:
        raise PermissionError("denied source")

    monkeypatch.setattr(tokenize, "open", denied)
    result = _execute(tmp_path)
    assert result.status is QualityStatus.ERROR
    assert "denied source" in result.diagnostics[0]


def test_target_path_controls_scan_independently_of_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "target"
    decoy = tmp_path / "decoy"
    _source(target, "import familyos_cli.infrastructure")
    _source(decoy, "pass")
    monkeypatch.chdir(decoy)
    assert _execute(target).status is QualityStatus.FAIL
