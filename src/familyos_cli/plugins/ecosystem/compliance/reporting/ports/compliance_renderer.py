"""Compliance report renderer port."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.ecosystem.compliance.reporting.compliance_report import (
    ComplianceReport,
)


class ComplianceRenderer(ABC):
    """Contract for a compliance report renderer.

    A renderer projects the canonical ComplianceReport into a
    presentation format; it must never recompute or reinterpret
    compliance status, rule outcomes, or severities.
    """

    @abstractmethod
    def render(
        self,
        report: ComplianceReport,
    ) -> str:
        """Render the report to its string representation."""

        raise NotImplementedError
