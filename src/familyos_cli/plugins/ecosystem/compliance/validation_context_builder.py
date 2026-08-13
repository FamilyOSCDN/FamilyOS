"""Validation context construction."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from familyos_cli.plugins.ecosystem.compliance.plugin_classification_resolver import (
    PluginClassificationResolver,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context import (
    ValidationContext,
)
from familyos_cli.plugins.models import PluginDescriptor


class ValidationContextBuilder:
    """Build a ValidationContext for a plugin, parsing its manifest once."""

    def __init__(
        self,
        *,
        discovery_root: Path,
    ) -> None:
        """Initialize the builder with the official plugins discovery root."""

        self._discovery_root = discovery_root

    def build(
        self,
        descriptor: PluginDescriptor,
    ) -> ValidationContext:
        """Build the validation context for the given plugin descriptor."""

        manifest, manifest_error = self._read_manifest(descriptor.path)

        classification = PluginClassificationResolver.classify(
            descriptor,
            self._discovery_root,
        )

        return ValidationContext(
            plugin_descriptor=descriptor,
            plugin_metadata=descriptor.metadata,
            classification=classification,
            manifest=manifest,
            manifest_error=manifest_error,
        )

    @staticmethod
    def _read_manifest(
        plugin_path: Path,
    ) -> tuple[Mapping[str, Any] | None, str | None]:
        """Read and parse the plugin manifest, returning data or an error."""

        manifest_file = plugin_path / "plugin.yaml"

        if not manifest_file.exists():
            return None, f"Manifest file not found: {manifest_file}"

        try:
            data = yaml.safe_load(
                manifest_file.read_text(encoding="utf-8"),
            )
        except yaml.YAMLError as error:
            return None, f"Manifest failed to parse: {error}"

        if not isinstance(data, dict):
            return None, "Manifest did not parse as a mapping"

        return data, None
