"""Tests for the machine-readable compliance report renderer."""

import json

from familyos_cli.plugins.ecosystem.compliance.reporting.json_compliance_renderer import (
    JsonComplianceRenderer,
)
from tests.unit.plugins.ecosystem.compliance.reporting.reporting_fixtures import (
    build_sample_report,
)


def test_render_produces_valid_json_with_schema_version() -> None:
    """The JSON renderer output round-trips and carries a schema version."""

    rendered = JsonComplianceRenderer().render(build_sample_report(with_finding=True))

    payload = json.loads(rendered)

    assert payload["schema_version"] == "1.0.0"
    assert payload["status"] == "non_compliant"
    assert payload["findings"][0]["rule_id"] == "PLUGIN-TEST-001"
    assert payload["rule_evaluations"][0]["outcome"] == "fail"
