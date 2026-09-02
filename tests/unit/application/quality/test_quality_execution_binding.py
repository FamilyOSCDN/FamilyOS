import pytest

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_execution_binding import (
    QualityExecutionBinding,
)
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)


class StubExecutor(QualityExecutorPort):
    def execute(self, *, check_id: QualityCheckId, rule: QualityRule, target: QualityTarget) -> QualityCheckResult:
        return QualityCheckResult(check_id=check_id, status=QualityStatus.PASS)

def rule() -> QualityRule:
    return QualityRule(QualityRuleId("QLT-RULE-TEST-001"), None, QualityDomain("QLT-DOM-TST"), QualitySeverity.HIGH, "Test rule.", "test")

def test_binding_preserves_explicit_components() -> None:
    check_id = QualityCheckId("QLT-CHECK-TEST")
    quality_rule = rule()
    executor = StubExecutor()
    binding = QualityExecutionBinding(check_id, quality_rule, executor)
    assert binding.check_id == check_id
    assert binding.rule == quality_rule
    assert binding.executor is executor

@pytest.mark.parametrize(("field", "value", "message"), (("check_id", "bad", "check_id must be a QualityCheckId"), ("rule", "bad", "rule must be a QualityRule"), ("executor", object(), "executor must implement QualityExecutorPort")))
def test_binding_rejects_invalid_dependencies(field: str, value: object, message: str) -> None:
    values = {"check_id": QualityCheckId("QLT-CHECK-TEST"), "rule": rule(), "executor": StubExecutor()}
    values[field] = value
    with pytest.raises(TypeError, match=message):
        QualityExecutionBinding(**values)  # type: ignore[arg-type]
