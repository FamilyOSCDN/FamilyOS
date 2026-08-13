"""Tests for the human-readable compliance report renderer."""

from familyos_cli.plugins.ecosystem.compliance.reporting.text_compliance_renderer import (
    TextComplianceRenderer,
)
from tests.unit.plugins.ecosystem.compliance.reporting.reporting_fixtures import (
    build_sample_report,
)


def test_render_compliant_report_shows_no_findings() -> None:
    """A compliant report with no findings renders 'Findings: none'."""

    rendered = TextComplianceRenderer().render(build_sample_report(with_finding=False))

    assert "Status: COMPLIANT" in rendered
    assert "Findings: none" in rendered


def test_render_non_compliant_report_shows_finding_detail() -> None:
    """A non-compliant report renders the finding's rule id and remediation."""

    rendered = TextComplianceRenderer().render(build_sample_report(with_finding=True))

    assert "Status: NON_COMPLIANT" in rendered
    assert "PLUGIN-TEST-001" in rendered
    assert "Remediation: Fix it." in rendered
