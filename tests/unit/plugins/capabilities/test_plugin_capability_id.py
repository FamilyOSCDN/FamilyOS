"""Tests for plugin capability identifiers."""

import pytest

from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


def test_plugin_capability_id_creation() -> None:
    """Canonical capability identifiers should preserve their value."""

    capability_id = PluginCapabilityId(
        "familyos.education.course",
    )

    assert capability_id.value == "familyos.education.course"
    assert str(capability_id) == "familyos.education.course"


def test_third_party_plugin_capability_id_creation() -> None:
    """Third-party capability namespaces should be supported."""

    capability_id = PluginCapabilityId(
        "acme.backup.archive",
    )

    assert capability_id.value == "acme.backup.archive"
    assert str(capability_id) == "acme.backup.archive"


def test_plugin_capability_id_rejects_empty_value() -> None:
    """Capability identifiers should reject empty values."""

    with pytest.raises(
        ValueError,
        match="Plugin capability id cannot be empty.",
    ):
        PluginCapabilityId("")


@pytest.mark.parametrize(
    "value",
    [
        "domain_generation",
        "templates",
        "FamilyOS.health.record",
        "familyos health record",
        "familyos.health",
        ".familyos.health.record",
        "familyos.health.record.",
        "familyos..health.record",
    ],
)
def test_plugin_capability_id_rejects_invalid_syntax(
    value: str,
) -> None:
    """Capability identifiers should require canonical syntax."""

    with pytest.raises(
        ValueError,
        match="Invalid plugin capability id",
    ):
        PluginCapabilityId(value)
