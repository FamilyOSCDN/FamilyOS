"""Compliance profile model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.severity import Severity


@dataclass(frozen=True, slots=True)
class ComplianceProfile:
    """Represent a governed selection and composition of compliance rules.

    A profile selects rules; it never redefines their meaning. See
    docs/epics/EPIC-PLUGIN-002-plugin-compliance-framework/
    07-Compliance-Profiles.md.
    """

    id: str
    version: str
    description: str
    included_rule_ids: tuple[str, ...]
    excluded_rule_ids: tuple[str, ...] = ()
    mandatory_rule_ids: tuple[str, ...] = ()
    blocking_severity_threshold: Severity = Severity.ERROR
