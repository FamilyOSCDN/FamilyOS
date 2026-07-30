"""Plugin contribution provider."""

from __future__ import annotations

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.plugin import Plugin


class PluginContributionProvider:
    """Extract contributions exposed by plugins."""

    def contributions(
        self,
        plugin: Plugin,
    ) -> tuple[Contribution, ...]:
        """Return every contribution exposed by a plugin."""

        contributions = plugin.contributions()

        if contributions:
            return self._normalize(
                contributions,
            )

        legacy_contributions: list[Contribution] = []

        legacy_contributions.extend(
            self._extract_legacy(
                plugin,
                "contribution",
            ),
        )

        legacy_contributions.extend(
            self._extract_legacy(
                plugin,
                "domain_contribution",
            ),
        )

        return tuple(
            legacy_contributions,
        )

    def _extract_legacy(
        self,
        plugin: Plugin,
        method_name: str,
    ) -> tuple[Contribution, ...]:
        """Extract contributions from a legacy plugin method."""

        method = getattr(
            plugin,
            method_name,
            None,
        )

        if not callable(
            method,
        ):
            return ()

        return self._normalize(
            method(),
        )

    def _normalize(
        self,
        value: object,
    ) -> tuple[Contribution, ...]:
        """Normalize one or multiple contribution values."""

        if isinstance(
            value,
            Contribution,
        ):
            return (
                value,
            )

        if isinstance(
            value,
            tuple,
        ):
            return tuple(
                item
                for item in value
                if isinstance(
                    item,
                    Contribution,
                )
            )

        return ()
