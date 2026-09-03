"""Contract tests for the canonical Quality executor application port."""

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)


class _StubQualityExecutor(QualityExecutorPort):
    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        assert isinstance(rule, QualityRule)
        assert isinstance(target, QualityTarget)
        return QualityCheckResult(
            check_id=check_id,
            status=QualityStatus.PASS,
        )


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-TEST-001"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-TST"),
        severity=QualitySeverity.MEDIUM,
        description="canonical contract test rule",
        executor="unit-test-executor",
    )


def test_executor_preserves_explicit_check_identity() -> None:
    check_id = QualityCheckId("QLT-CHECK-UNIT")

    result = _StubQualityExecutor().execute(
        check_id=check_id,
        rule=_rule(),
        target=QualityTarget(
            target_type="repository",
            identifier="familyos",
        ),
    )

    assert result.check_id is check_id
    assert result.status is QualityStatus.PASS


def test_executor_port_is_abstract() -> None:
    try:
        QualityExecutorPort()  # type: ignore[abstract]
    except TypeError:
        return

    raise AssertionError("QualityExecutorPort must remain abstract")
