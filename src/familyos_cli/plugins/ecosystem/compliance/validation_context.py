"""Validation context model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.models import PluginDescriptor, PluginMetadata


@dataclass(frozen=True, slots=True)
class ValidationContext:
    """Represent the explicit context for one compliance evaluation.

    Built once per evaluation by
    :class:`~familyos_cli.plugins.ecosystem.compliance.validation_context_builder.ValidationContextBuilder`
    so validators reading the manifest do not each repeat file I/O.
    """

    plugin_descriptor: PluginDescriptor
    plugin_metadata: PluginMetadata
    classification: PluginClassification
    manifest: Mapping[str, Any] | None
    manifest_error: str | None
