"""Shared fixtures for compliance validator tests."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.models import PluginDescriptor


def make_descriptor(
    plugin_path: Path,
    *,
    plugin_id: str = "familyos.fixture",
    version: str = "1.0.0",
    module: str = "tests.fixtures.sample_plugin.plugin",
    class_name: str = "SamplePlugin",
) -> PluginDescriptor:
    """Build a PluginDescriptor pointing at a filesystem path."""

    return PluginDescriptor(
        id=plugin_id,
        name="Fixture Plugin",
        version=version,
        module=module,
        class_name=class_name,
        path=plugin_path,
    )


def make_context(
    plugin_path: Path,
    *,
    manifest: dict[str, object] | None,
    manifest_error: str | None = None,
    plugin_id: str = "familyos.fixture",
    version: str = "1.0.0",
    module: str = "tests.fixtures.sample_plugin.plugin",
    class_name: str = "SamplePlugin",
    classification: PluginClassification = PluginClassification.OFFICIAL,
) -> ValidationContext:
    """Build a ValidationContext without touching the filesystem manifest."""

    descriptor = make_descriptor(
        plugin_path,
        plugin_id=plugin_id,
        version=version,
        module=module,
        class_name=class_name,
    )

    return ValidationContext(
        plugin_descriptor=descriptor,
        plugin_metadata=descriptor.metadata,
        classification=classification,
        manifest=manifest,
        manifest_error=manifest_error,
    )
