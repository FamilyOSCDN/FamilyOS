"""Tests for the validation context model."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.models import PluginDescriptor


def test_validation_context_construction() -> None:
    """A ValidationContext stores every provided field."""

    descriptor = PluginDescriptor(
        id="familyos.test",
        name="Test",
        version="1.0.0",
        module="tests.fixtures.test.plugin",
        class_name="TestPlugin",
        path=Path("/tmp/familyos.test"),
    )

    context = ValidationContext(
        plugin_descriptor=descriptor,
        plugin_metadata=descriptor.metadata,
        classification=PluginClassification.OFFICIAL,
        manifest={"id": "familyos.test"},
        manifest_error=None,
    )

    assert context.classification is PluginClassification.OFFICIAL
    assert context.manifest == {"id": "familyos.test"}
