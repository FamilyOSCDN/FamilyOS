"""Normalized result of a canonical Quality check execution."""

from dataclasses import dataclass

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityEvidence,
    QualityFinding,
    QualityStatus,
)


@dataclass(frozen=True, slots=True)
class QualityCheckResult:
    """Tool-independent normalized Quality check result."""

    check_id: QualityCheckId
    status: QualityStatus
    findings: tuple[QualityFinding, ...] = ()
    evidence: tuple[QualityEvidence, ...] = ()
    duration_seconds: float = 0.0
    diagnostics: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.check_id, QualityCheckId):
            raise TypeError("QualityCheckResult check_id must be a QualityCheckId")
        if not isinstance(self.status, QualityStatus):
            raise TypeError("QualityCheckResult status must be a QualityStatus")
        if not isinstance(self.findings, tuple):
            raise TypeError("QualityCheckResult findings must be a tuple")
        if not all(isinstance(item, QualityFinding) for item in self.findings):
            raise TypeError(
                "QualityCheckResult findings must contain QualityFinding values"
            )
        if not isinstance(self.evidence, tuple):
            raise TypeError("QualityCheckResult evidence must be a tuple")
        if not all(isinstance(item, QualityEvidence) for item in self.evidence):
            raise TypeError(
                "QualityCheckResult evidence must contain QualityEvidence values"
            )
        if isinstance(self.duration_seconds, bool) or not isinstance(
            self.duration_seconds, (int, float)
        ):
            raise TypeError("QualityCheckResult duration_seconds must be numeric")
        if self.duration_seconds < 0:
            raise ValueError(
                "QualityCheckResult duration_seconds must be non-negative"
            )
        if not isinstance(self.diagnostics, tuple):
            raise TypeError("QualityCheckResult diagnostics must be a tuple")
        for diagnostic in self.diagnostics:
            if not isinstance(diagnostic, str):
                raise TypeError(
                    "QualityCheckResult diagnostics must contain str values"
                )
            if not diagnostic:
                raise ValueError(
                    "QualityCheckResult diagnostics must contain non-empty strings"
                )
