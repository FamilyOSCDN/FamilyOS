"""Machine-readable (JSON) compliance report renderer."""

from __future__ import annotations

import json
from typing import Any

from familyos_cli.plugins.ecosystem.compliance.reporting.compliance_report import (
    ComplianceReport,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.ports.compliance_renderer import (
    ComplianceRenderer,
)


class JsonComplianceRenderer(ComplianceRenderer):
    """Render a compliance report as machine-readable JSON."""

    def render(
        self,
        report: ComplianceReport,
    ) -> str:
        """Return a JSON rendering of the report."""

        result = report.result

        payload: dict[str, Any] = {
            "schema_version": report.schema_version,
            "framework_version": report.framework_version,
            "profile_version": report.profile_version,
            "evaluation_id": result.evaluation_id,
            "plugin_id": result.plugin_id,
            "plugin_version": result.plugin_version,
            "profile_id": result.profile_id,
            "status": result.status.value,
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat(),
            "rule_evaluations": [
                {
                    "rule_id": evaluation.rule_id,
                    "domain": evaluation.domain.value,
                    "outcome": evaluation.outcome.value,
                    "severity": evaluation.severity.value,
                    "validator_status": evaluation.validator_status.value,
                    "evidence_refs": list(evaluation.evidence_refs),
                    "message": evaluation.message,
                    "mandatory": evaluation.mandatory,
                }
                for evaluation in result.rule_evaluations
            ],
            "findings": [
                {
                    "id": finding.id,
                    "rule_id": finding.rule_id,
                    "domain": finding.domain.value,
                    "severity": finding.severity.value,
                    "category": finding.category.value,
                    "status": finding.status.value,
                    "title": finding.title,
                    "message": finding.message,
                    "evidence_refs": list(finding.evidence_refs),
                    "location": finding.location,
                    "remediation": finding.remediation,
                }
                for finding in result.findings
            ],
            "evidence": [
                {
                    "id": evidence.id,
                    "type": evidence.type.value,
                    "source": evidence.source,
                    "producer": evidence.producer,
                    "producer_version": evidence.producer_version,
                    "scope": evidence.scope,
                    "trust_level": evidence.trust_level.value,
                    "collected_at": evidence.collected_at.isoformat(),
                }
                for evidence in result.evidence
            ],
        }

        return json.dumps(payload, indent=2, sort_keys=False)
