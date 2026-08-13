"""Compliance validation request model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.models import PluginDescriptor


@dataclass(frozen=True, slots=True)
class ComplianceRequest:
    """Represent a request to evaluate one plugin against one profile."""

    plugin_descriptor: PluginDescriptor
    profile_id: str = "official"
