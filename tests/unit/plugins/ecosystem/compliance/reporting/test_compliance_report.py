"""Tests for the compliance report model."""

from tests.unit.plugins.ecosystem.compliance.reporting.reporting_fixtures import (
    build_sample_report,
)


def test_compliance_report_wraps_result() -> None:
    """A ComplianceReport carries the wrapped ComplianceResult."""

    report = build_sample_report(with_finding=False)

    assert report.result.plugin_id == "familyos.test"
    assert report.schema_version == "1.0.0"
