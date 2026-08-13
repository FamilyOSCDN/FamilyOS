"""Plugin fixture that deliberately violates several compliance rules.

Used by compliance validator unit tests to exercise capability namespace,
capability uniqueness, and contribution path FAIL outcomes without
needing separate fixture plugins per rule.
"""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins import Plugin
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)
from familyos_cli.plugins.contributions.contribution import Contribution
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.plugin_metadata import PluginMetadata


class ViolationPlugin(Plugin):
    """Plugin used to exercise compliance validator FAIL outcomes."""

    metadata = PluginMetadata(
        name="Violation Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Plugin used for compliance validator FAIL tests.",
    )

    def capabilities(self) -> tuple[PluginCapability, ...]:
        """Return capabilities violating namespace and uniqueness rules."""

        return (
            PluginCapability(
                id=PluginCapabilityId("other.plugin.capability"),
                display_name="",
            ),
            PluginCapability(
                id=PluginCapabilityId("familyos.violation.dup"),
                display_name="Duplicate",
            ),
            PluginCapability(
                id=PluginCapabilityId("familyos.violation.dup2"),
                display_name="Duplicate",
            ),
        )

    def contributions(self) -> tuple[Contribution, ...]:
        """Return a template contribution pointing at a missing directory."""

        return (
            TemplateContribution(
                id=PluginContributionId("familyos.violation.template"),
                template_directory=Path("this/path/does/not/exist"),
            ),
        )
