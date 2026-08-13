"""Tests for the compliance request model."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.models import PluginDescriptor


def test_compliance_request_defaults_to_official_profile() -> None:
    """A ComplianceRequest defaults to the official profile."""

    descriptor = PluginDescriptor(
        id="familyos.test",
        name="Test",
        version="1.0.0",
        module="tests.fixtures.test.plugin",
        class_name="TestPlugin",
        path=Path("/tmp/familyos.test"),
    )

    request = ComplianceRequest(plugin_descriptor=descriptor)

    assert request.profile_id == "official"
