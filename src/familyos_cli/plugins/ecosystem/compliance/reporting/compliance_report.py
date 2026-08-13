"""Compliance report model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.compliance_result import (
    ComplianceResult,
)

REPORT_SCHEMA_VERSION = "1.0.0"
COMPLIANCE_FRAMEWORK_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class ComplianceReport:
    """Wrap a ComplianceResult with report and framework version context.

    ``schema_version`` identifies the report wire format and is
    intentionally distinct from ``framework_version`` and
    ``profile_version`` (see docs/epics/EPIC-PLUGIN-002.../
    11-Compliance-Reporting.md).
    """

    schema_version: str
    framework_version: str
    profile_version: str
    result: ComplianceResult
