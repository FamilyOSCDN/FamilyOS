"""Human-readable compliance report renderer."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.compliance_report import (
    ComplianceReport,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.ports.compliance_renderer import (
    ComplianceRenderer,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity

_SEVERITY_ORDER: dict[Severity, int] = {
    Severity.CRITICAL: 0,
    Severity.ERROR: 1,
    Severity.WARNING: 2,
    Severity.INFO: 3,
}


def _finding_sort_key(finding: ComplianceFinding) -> tuple[int, str]:
    return (_SEVERITY_ORDER[finding.severity], finding.rule_id)


class TextComplianceRenderer(ComplianceRenderer):
    """Render a compliance report as human-readable text."""

    def render(
        self,
        report: ComplianceReport,
    ) -> str:
        """Return a human-readable rendering of the report."""

        result = report.result

        lines: list[str] = [
            f"Plugin: {result.plugin_id}",
            f"Version: {result.plugin_version}",
            f"Profile: {result.profile_id} ({report.profile_version})",
            f"Framework: {report.framework_version}",
            f"Status: {result.status.value.upper()}",
            "",
        ]

        counts = dict.fromkeys(Severity, 0)
        for finding in result.findings:
            counts[finding.severity] += 1

        lines.append(f"Critical: {counts[Severity.CRITICAL]}")
        lines.append(f"Errors: {counts[Severity.ERROR]}")
        lines.append(f"Warnings: {counts[Severity.WARNING]}")
        lines.append(f"Info: {counts[Severity.INFO]}")
        lines.append("")

        if not result.findings:
            lines.append("Findings: none")
        else:
            lines.append("Findings:")
            lines.append("")

            for finding in sorted(result.findings, key=_finding_sort_key):
                lines.extend(
                    [
                        f"{finding.severity.value.upper()}  {finding.rule_id}",
                        "",
                        finding.message,
                        "",
                        f"Remediation: {finding.remediation}",
                        "",
                    ],
                )

        return "\n".join(lines).rstrip() + "\n"
