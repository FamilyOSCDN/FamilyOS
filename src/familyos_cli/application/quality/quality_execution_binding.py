"""Narrow Phase 12 execution binding."""
from dataclasses import dataclass

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.domain.quality import QualityCheckId, QualityRule


@dataclass(frozen=True, slots=True)
class QualityExecutionBinding:
    """Bind one governed check to its rule and executor port."""
    check_id: QualityCheckId
    rule: QualityRule
    executor: QualityExecutorPort

    def __post_init__(self) -> None:
        if not isinstance(self.check_id, QualityCheckId):
            raise TypeError("check_id must be a QualityCheckId")
        if not isinstance(self.rule, QualityRule):
            raise TypeError("rule must be a QualityRule")
        if not isinstance(self.executor, QualityExecutorPort):
            raise TypeError("executor must implement QualityExecutorPort")
