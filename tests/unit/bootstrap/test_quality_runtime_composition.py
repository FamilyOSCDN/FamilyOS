from pathlib import Path

from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.bootstrap.container import ApplicationContainer
from familyos_cli.domain.quality import QualityEvidenceId, QualityFindingId
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
