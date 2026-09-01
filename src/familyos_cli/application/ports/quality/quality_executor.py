"""Application port for tool-independent Quality check execution."""

from abc import ABC, abstractmethod

from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import QualityCheckId, QualityRule, QualityTarget


class QualityExecutorPort(ABC):
    """Execute a governed Quality check without exposing tool-specific details."""

    @abstractmethod
    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        """Execute the governed check and return its normalized result."""

        raise NotImplementedError
