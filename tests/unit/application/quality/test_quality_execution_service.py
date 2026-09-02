from __future__ import annotations

import pytest

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_execution_binding import (
    QualityExecutionBinding,
)
from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.application.quality.quality_profile_registry import (
    QualityProfileRegistry,
)
from familyos_cli.application.quality.quality_profile_resolver import (
    QualityProfileResolver,
)
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityProfile,
    QualityProfileId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)

TARGET = QualityTarget("repository", "familyos-cli", revision="abc123")
CHECK_A = QualityCheckId("QLT-CHECK-A")
CHECK_B = QualityCheckId("QLT-CHECK-B")


class RecordingExecutor(QualityExecutorPort):
    def __init__(
        self,
        *,
        status: QualityStatus = QualityStatus.PASS,
        returned_check_id: QualityCheckId | None = None,
    ) -> None:
        self.status = status
        self.returned_check_id = returned_check_id
        self.calls: list[tuple[QualityCheckId, QualityRule, QualityTarget]] = []

    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        self.calls.append((check_id, rule, target))
        return QualityCheckResult(
            check_id=self.returned_check_id or check_id,
            status=self.status,
        )


def rule(rule_id: str) -> QualityRule:
    return QualityRule(
        id=QualityRuleId(rule_id),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.HIGH,
        description="Execution service test rule.",
        executor="test",
    )


def resolver_for(
    required_checks: tuple[QualityCheckId, ...],
    *,
    target_types: tuple[str, ...] = ("repository",),
) -> QualityProfileResolver:
    registry = QualityProfileRegistry()
    registry.register(
        QualityProfile(
            id=QualityProfileId("QLT-PROFILE-TEST"),
            version="1.0.0",
            target_types=target_types,
            required_checks=required_checks,
            required_domains=(),
            severity_policy=(),
        )
    )
    return QualityProfileResolver(registry)


def binding(
    check_id: QualityCheckId,
    executor: QualityExecutorPort,
    *,
    rule_id: str,
) -> QualityExecutionBinding:
    return QualityExecutionBinding(
        check_id=check_id,
        rule=rule(rule_id),
        executor=executor,
    )


def test_executes_required_checks_in_profile_order_not_binding_order() -> None:
    executor_a = RecordingExecutor()
    executor_b = RecordingExecutor()
    service = QualityExecutionService(
        resolver_for((CHECK_B, CHECK_A)),
        (
            binding(CHECK_A, executor_a, rule_id="QLT-RULE-A"),
            binding(CHECK_B, executor_b, rule_id="QLT-RULE-B"),
        ),
    )

    results = service.execute(TARGET)

    assert tuple(result.check_id for result in results) == (CHECK_B, CHECK_A)
    assert executor_b.calls[0][0] == CHECK_B
    assert executor_a.calls[0][0] == CHECK_A


def test_passes_exact_check_rule_and_target_to_executor() -> None:
    executor = RecordingExecutor()
    expected_rule = rule("QLT-RULE-A")
    service = QualityExecutionService(
        resolver_for((CHECK_A,)),
        (
            QualityExecutionBinding(
                check_id=CHECK_A,
                rule=expected_rule,
                executor=executor,
            ),
        ),
    )

    service.execute(TARGET)

    assert executor.calls == [(CHECK_A, expected_rule, TARGET)]


def test_preserves_normalized_executor_result() -> None:
    executor = RecordingExecutor(status=QualityStatus.WARNING)
    service = QualityExecutionService(
        resolver_for((CHECK_A,)),
        (binding(CHECK_A, executor, rule_id="QLT-RULE-A"),),
    )

    result = service.execute(TARGET)

    assert len(result) == 1
    assert result[0].status is QualityStatus.WARNING


def test_missing_required_binding_fails_explicitly() -> None:
    service = QualityExecutionService(
        resolver_for((CHECK_A, CHECK_B)),
        (binding(CHECK_A, RecordingExecutor(), rule_id="QLT-RULE-A"),),
    )

    with pytest.raises(
        ValueError,
        match="No QualityExecutionBinding exists for required check QLT-CHECK-B",
    ):
        service.execute(TARGET)


def test_duplicate_binding_check_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="bindings must contain unique check_ids"):
        QualityExecutionService(
            resolver_for((CHECK_A,)),
            (
                binding(CHECK_A, RecordingExecutor(), rule_id="QLT-RULE-A"),
                binding(CHECK_A, RecordingExecutor(), rule_id="QLT-RULE-B"),
            ),
        )


def test_unresolved_profile_failure_is_preserved() -> None:
    service = QualityExecutionService(
        resolver_for((CHECK_A,), target_types=("documentation",)),
        (binding(CHECK_A, RecordingExecutor(), rule_id="QLT-RULE-A"),),
    )

    with pytest.raises(ValueError, match="No QualityProfile applies"):
        service.execute(TARGET)


def test_executor_result_for_different_check_is_rejected() -> None:
    executor = RecordingExecutor(returned_check_id=CHECK_B)
    service = QualityExecutionService(
        resolver_for((CHECK_A,)),
        (binding(CHECK_A, executor, rule_id="QLT-RULE-A"),),
    )

    with pytest.raises(
        ValueError,
        match="executor result check_id must match the required QualityCheckId",
    ):
        service.execute(TARGET)


def test_constructor_rejects_invalid_dependencies() -> None:
    resolver = resolver_for((CHECK_A,))
    valid_bindings = (
        binding(CHECK_A, RecordingExecutor(), rule_id="QLT-RULE-A"),
    )

    with pytest.raises(TypeError, match="profile_resolver"):
        QualityExecutionService(object(), valid_bindings)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="bindings"):
        QualityExecutionService(resolver, [])  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="bindings"):
        QualityExecutionService(
            resolver,
            (object(),),  # type: ignore[arg-type]
        )


def test_execute_rejects_invalid_target() -> None:
    service = QualityExecutionService(resolver_for(()), ())

    with pytest.raises(TypeError, match="target must be a QualityTarget"):
        service.execute(object())  # type: ignore[arg-type]
