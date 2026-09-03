from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import pytest

from familyos_cli.infrastructure.documentation import (
    DocumentationValidationResult,
    DocumentationValidator,
    DocumentationViolation,
)

_ROOTS = ("docs/epics/EPIC-B", "docs/epics/EPIC-A")


def _write_epic(root: Path, content: str = "# Valid document\n") -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "EPIC.yaml").write_text(
        json.dumps({
            "deliverables": ["EPIC.yaml", "README.md"],
            "structure": {
                "numbered_documents": 0,
                "canonical_document_range": "none",
                "control_documents": 2,
                "canonical_files": 2,
            },
        }),
        encoding="utf-8",
    )
    (root / "README.md").write_text(content, encoding="utf-8")


@pytest.mark.parametrize(
    ("scope", "error"),
    [
        (None, TypeError),
        (["docs/epics/EPIC-A"], TypeError),
        ("docs/epics/EPIC-A", TypeError),
        ((42,), TypeError),
        ((), ValueError),
        (("",), ValueError),
        (("docs/epics/EPIC-A", "docs/epics/EPIC-A"), ValueError),
        (("/docs/epics/EPIC-A",), ValueError),
        (("docs/epics/../EPIC-A",), ValueError),
        (("docs/epics/.",), ValueError),
        (("docs/epics/..",), ValueError),
        (("./docs/epics/EPIC-A",), ValueError),
        (("docs//epics/EPIC-A",), ValueError),
        (("docs/epics/",), ValueError),
        (("docs/epics/EPIC-A/",), ValueError),
        (("docs/epics/EPIC-A/nested",), ValueError),
        (("other/epics/EPIC-A",), ValueError),
        ((r"docs\epics\EPIC-A",), ValueError),
        (("docs/epics/EPIC-\nA",), ValueError),
        (("docs/epics/EPIC-\tA",), ValueError),
        (("docs/epics/EPIC-\0A",), ValueError),
        (("docs/epics/EPIC-\x7fA",), ValueError),
        (("docs/epics/EPIC-\x85A",), ValueError),
    ],
)
def test_invalid_scope_is_rejected_before_epic_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    scope: object, error: type[Exception],
) -> None:
    validator = DocumentationValidator()

    def unexpected_validation(root: Path) -> DocumentationValidationResult:
        pytest.fail("An invalid scope must not reach document validation")

    monkeypatch.setattr(validator, "validate", unexpected_validation)
    with pytest.raises(error):
        validator.validate_repository(tmp_path, epic_roots=cast(tuple[str, ...], scope))


def test_only_explicit_epics_are_checked(tmp_path: Path) -> None:
    for relative in _ROOTS:
        _write_epic(tmp_path / relative)
    _write_epic(tmp_path / "docs/epics/UNLISTED", "No heading\n")
    (tmp_path / "EPIC.yaml").write_text("malformed: [", encoding="utf-8")

    result = DocumentationValidator().validate_repository(tmp_path, epic_roots=_ROOTS)

    assert result.violations == ()


def test_multiple_epics_keep_configured_order_and_repeated_findings(tmp_path: Path) -> None:
    for relative in _ROOTS:
        _write_epic(tmp_path / relative, "No heading\n")

    result = DocumentationValidator().validate_repository(tmp_path, epic_roots=_ROOTS)

    assert [v.location for v in result.violations] == [
        f"{relative}/README.md" for relative in _ROOTS
    ]
    assert len(result.violations) == 2
    assert result.violations[0].message == result.violations[1].message


def test_location_suffixes_and_missing_location_are_preserved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    validator = DocumentationValidator()
    calls: list[Path] = []
    suffixes = ("README.md:7", "00-A.md, 00-B.md", None)

    def validate(root: Path) -> DocumentationValidationResult:
        calls.append(root)
        return DocumentationValidationResult(tuple(
            DocumentationViolation("example", "Original message", suffix)
            for suffix in suffixes
        ))

    monkeypatch.setattr(validator, "validate", validate)
    result = validator.validate_repository(tmp_path, epic_roots=_ROOTS)

    assert calls == [tmp_path / relative for relative in _ROOTS]
    assert [(v.kind, v.message, v.location) for v in result.violations] == [
        ("example", "Original message", f"{relative}/{suffix}" if suffix else relative)
        for relative in _ROOTS for suffix in suffixes
    ]


@pytest.mark.parametrize("problem", ["missing-directory", "missing-manifest", "invalid-yaml"])
def test_missing_or_invalid_selected_inventory_is_a_violation(
    tmp_path: Path, problem: str,
) -> None:
    broken = tmp_path / _ROOTS[0]
    if problem != "missing-directory":
        broken.mkdir(parents=True)
    if problem == "invalid-yaml":
        (broken / "EPIC.yaml").write_text("invalid: [", encoding="utf-8")
    _write_epic(tmp_path / _ROOTS[1])

    result = DocumentationValidator().validate_repository(tmp_path, epic_roots=_ROOTS)

    assert len(result.violations) == 1
    assert result.violations[0].location == f"{_ROOTS[0]}/EPIC.yaml"
    assert result.violations[0].kind == (
        "epic_yaml" if problem == "invalid-yaml" else "required_file"
    )


@pytest.mark.parametrize("error", [PermissionError, OSError, RuntimeError])
def test_validator_failures_propagate_without_partial_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, error: type[Exception],
) -> None:
    validator = DocumentationValidator()
    calls: list[Path] = []

    def validate(root: Path) -> DocumentationValidationResult:
        calls.append(root)
        if root == tmp_path / _ROOTS[1]:
            raise error("cannot read selected EPIC")
        return DocumentationValidationResult((DocumentationViolation("test", "Violation"),))

    monkeypatch.setattr(validator, "validate", validate)
    with pytest.raises(error, match="cannot read"):
        validator.validate_repository(tmp_path, epic_roots=_ROOTS)
    assert calls == [tmp_path / relative for relative in _ROOTS]


def test_selected_symlink_must_not_escape_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = tmp_path / "repository"
    selected = repository / _ROOTS[0]
    selected.parent.mkdir(parents=True)
    outside = tmp_path / "outside"
    _write_epic(outside)
    selected.symlink_to(outside, target_is_directory=True)
    validator = DocumentationValidator()

    def unexpected_validation(root: Path) -> DocumentationValidationResult:
        pytest.fail("An escaping selected root must not be validated")

    monkeypatch.setattr(validator, "validate", unexpected_validation)
    with pytest.raises(ValueError, match="outside the target"):
        validator.validate_repository(repository, epic_roots=(_ROOTS[0],))


@pytest.mark.parametrize("is_file", [False, True])
def test_repository_root_must_be_an_accessible_directory(
    tmp_path: Path, is_file: bool,
) -> None:
    root = tmp_path / "not-a-directory"
    if is_file:
        root.write_text("file", encoding="utf-8")
    with pytest.raises(ValueError, match="not a directory"):
        DocumentationValidator().validate_repository(root, epic_roots=_ROOTS)
