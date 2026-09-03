import json
from pathlib import Path

import pytest

from familyos_cli.application.quality.initial_repository_documentation_scope import (
    INITIAL_REPOSITORY_DOCUMENTATION_ROOTS,
)
from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.bootstrap.container import ApplicationContainer
from familyos_cli.domain.quality import (
    QualityAssessmentState,
    QualityCheckId,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityFindingId,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.documentation import (
    DocumentationValidationResult,
    DocumentationValidator,
)
from familyos_cli.infrastructure.quality.documentation_quality_executor import (
    DocumentationQualityExecutor,
)
from familyos_cli.infrastructure.quality.mypy_quality_executor import (
    MypyQualityExecutor,
)
from familyos_cli.infrastructure.quality.plugin_compliance_quality_executor import (
    PluginComplianceQualityExecutor,
)
from familyos_cli.infrastructure.quality.pytest_quality_executor import (
    PytestQualityExecutor,
)
from familyos_cli.infrastructure.quality.ruff_quality_executor import (
    RuffQualityExecutor,
)


def test_container_composes_quality_execution_service(tmp_path: Path) -> None:
    service = ApplicationContainer(project_root=tmp_path).quality_execution_service()
    assert isinstance(service, QualityExecutionService)


def test_container_composes_exact_governed_executor_bindings(tmp_path: Path) -> None:
    service = ApplicationContainer(project_root=tmp_path).quality_execution_service()
    bindings = service._bindings  # noqa: SLF001
    assert tuple(str(check_id) for check_id in bindings) == (
        "QLT-CHECK-RUFF",
        "QLT-CHECK-MYPY",
        "QLT-CHECK-PYTEST",
        "QLT-CHECK-DOC",
        "QLT-CHECK-PLUGIN-COMPLIANCE",
    )
    by_id = {str(check_id): binding.executor for check_id, binding in bindings.items()}
    assert isinstance(by_id["QLT-CHECK-RUFF"], RuffQualityExecutor)
    assert isinstance(by_id["QLT-CHECK-MYPY"], MypyQualityExecutor)
    assert isinstance(by_id["QLT-CHECK-PYTEST"], PytestQualityExecutor)
    assert isinstance(by_id["QLT-CHECK-DOC"], DocumentationQualityExecutor)
    assert isinstance(
        by_id["QLT-CHECK-PLUGIN-COMPLIANCE"], PluginComplianceQualityExecutor
    )


def test_container_runtime_quality_ids_are_valid_and_opaque() -> None:
    first_finding = ApplicationContainer._quality_finding_id()
    second_finding = ApplicationContainer._quality_finding_id()
    first_evidence = ApplicationContainer._quality_evidence_id()
    second_evidence = ApplicationContainer._quality_evidence_id()
    assert isinstance(first_finding, QualityFindingId)
    assert isinstance(first_evidence, QualityEvidenceId)
    assert str(first_finding).startswith("QLT-FIND-")
    assert str(first_evidence).startswith("QLT-EVID-")
    assert first_finding != second_finding
    assert first_evidence != second_evidence


def test_plugin_compliance_binding_reuses_container_engine(tmp_path: Path) -> None:
    container = ApplicationContainer(project_root=tmp_path)
    service = container.quality_execution_service()
    bindings = service._bindings  # noqa: SLF001
    by_id = {str(check_id): binding.executor for check_id, binding in bindings.items()}
    executor = by_id["QLT-CHECK-PLUGIN-COMPLIANCE"]
    assert isinstance(executor, PluginComplianceQualityExecutor)
    assert executor._engine is container._compliance_engine  # noqa: SLF001
    assert executor._plugins_root == container._builtin_plugins_root  # noqa: SLF001


def test_container_composes_quality_assessment_execution_service(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.quality.quality_assessment_execution_service import (
        QualityAssessmentExecutionService,
    )

    assert isinstance(
        ApplicationContainer(
            project_root=tmp_path
        ).quality_assessment_execution_service(),
        QualityAssessmentExecutionService,
    )


def test_container_quality_assessment_identity_and_clock() -> None:
    first = ApplicationContainer._quality_assessment_id()
    second = ApplicationContainer._quality_assessment_id()
    assert str(first).startswith("QLT-ASMT-")
    assert first != second
    now = ApplicationContainer._quality_assessment_clock()
    assert now.tzinfo is not None and now.utcoffset() is not None


def test_container_configures_the_frozen_repository_documentation_scope() -> None:
    service = ApplicationContainer().quality_execution_service()
    binding = service._bindings[QualityCheckId("QLT-CHECK-DOC")]  # noqa: SLF001
    executor = binding.executor
    assert isinstance(executor, DocumentationQualityExecutor)
    assert executor._repository_epic_roots == INITIAL_REPOSITORY_DOCUMENTATION_ROOTS  # noqa: SLF001


def test_documentation_scope_uses_target_path_independent_of_container_and_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = tmp_path / "explicit-target"
    decoy = tmp_path / "different-container-and-cwd"
    decoy.mkdir()
    for relative in INITIAL_REPOSITORY_DOCUMENTATION_ROOTS:
        epic = repository / relative
        epic.mkdir(parents=True)
        (epic / "README.md").write_text("# Valid EPIC\n", encoding="utf-8")
        (epic / "EPIC.yaml").write_text(
            json.dumps({
                "deliverables": ["EPIC.yaml", "README.md"],
                "structure": {
                    "numbered_documents": 0,
                    "canonical_document_range": "none",
                    "canonical_files": 2,
                    "control_documents": 2,
                },
            }),
            encoding="utf-8",
        )
    monkeypatch.chdir(decoy)
    service = ApplicationContainer(project_root=decoy).quality_execution_service()
    binding = service._bindings[QualityCheckId("QLT-CHECK-DOC")]  # noqa: SLF001
    target = QualityTarget(
        target_type="repository", identifier="explicit-target",
        path=str(repository), revision="explicit-revision",
    )

    result = binding.executor.execute(
        check_id=binding.check_id, rule=binding.rule, target=target,
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert result.evidence[0].target is target
    assert result.evidence[0].revision == "explicit-revision"
    assert result.evidence[0].metadata == (
        ("violations", "0"),
        ("scope", "repository_epics"),
        ("epic_roots", "\n".join(INITIAL_REPOSITORY_DOCUMENTATION_ROOTS)),
    )


def test_composed_assessment_retains_one_documentation_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    epic = tmp_path / "explicit-epic"
    epic.mkdir()
    (epic / "README.md").write_text("# First heading\n\n# Second heading\n", encoding="utf-8")
    (epic / "EPIC.yaml").write_text(
        json.dumps({
            "deliverables": ["EPIC.yaml", "README.md"],
            "structure": {
                "numbered_documents": 0,
                "canonical_document_range": "none",
                "canonical_files": 2,
                "control_documents": 2,
            },
        }),
        encoding="utf-8",
    )
    calls: list[Path] = []
    original_validate = DocumentationValidator.validate

    def validate(
        validator: DocumentationValidator, root: Path,
    ) -> DocumentationValidationResult:
        calls.append(root)
        return original_validate(validator, root)

    monkeypatch.setattr(DocumentationValidator, "validate", validate)
    target = QualityTarget(
        target_type="documentation", identifier="test-epic",
        revision="explicit-revision", path=str(epic),
    )
    service = ApplicationContainer(project_root=tmp_path).quality_assessment_execution_service()

    output = service.execute_with_results(target)

    assert len(output.check_results) == 1
    check = output.check_results[0]
    assert check.check_id == QualityCheckId("QLT-CHECK-DOC")
    assert check.status is QualityStatus.FAIL
    assert check.diagnostics == ()
    assert len(check.evidence) == len(check.findings) == 1
    evidence, finding = check.evidence[0], check.findings[0]
    assert evidence.target is finding.target is target
    assert evidence.revision == target.revision
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.source == "quality.documentation"
    assert evidence.metadata == (("violations", "1"),)
    assert finding.message == "Markdown document must contain exactly one level-one heading; found 2."
    assert finding.location == "README.md"
    assert finding.evidence_ids == (str(evidence.id),)
    assert output.assessment.target is target
    assert output.assessment.profile == "QLT-PROFILE-DOCUMENTATION@1.0.0"
    assert output.assessment.revision == target.revision
    assert output.assessment.evidence_ids == (evidence.id,)
    assert output.assessment.finding_ids == (finding.id,)
    assert output.assessment.status is QualityStatus.UNKNOWN
    assert output.assessment.quality_state is QualityAssessmentState.UNKNOWN
    assert calls == [epic]
