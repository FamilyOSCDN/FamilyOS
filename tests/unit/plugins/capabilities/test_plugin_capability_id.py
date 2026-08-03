"""Tests for plugin capability identifiers."""

import pytest

from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


def test_plugin_capability_id_creation() -> None:
    """Capability identifiers should preserve their value."""

    capability_id = PluginCapabilityId(
        "domain_generation",
    )

    assert capability_id.value == "domain_generation"
    assert str(capability_id) == "domain_generation"


def test_plugin_capability_id_rejects_empty_value() -> None:
    """Capability identifiers should reject empty values."""

    with pytest.raises(
        ValueError,
        match="Plugin capability id cannot be empty.",
    ):
        PluginCapabilityId("")
