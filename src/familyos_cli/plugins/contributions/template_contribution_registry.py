"""Template contribution registry."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)


class TemplateContributionRegistry:
    """Registry of plugin template contributions."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._contributions: dict[
            Path,
            TemplateContribution,
        ] = {}

    def register(
        self,
        contribution: TemplateContribution,
    ) -> None:
        """Register a template contribution."""

        if (
            contribution.template_directory
            in self._contributions
        ):
            raise ValueError(
                (
                    "Template contribution "
                    f"'{contribution.template_directory}' "
                    "already registered."
                ),
            )

        self._contributions[
            contribution.template_directory
        ] = contribution

    def get(
        self,
        directory: Path,
    ) -> TemplateContribution:
        """Return contribution for a directory."""

        return self._contributions[directory]

    def list(
        self,
    ) -> tuple[TemplateContribution, ...]:
        """Return registered contributions."""

        return tuple(
            self._contributions.values(),
        )

    def all(
        self,
    ) -> tuple[TemplateContribution, ...]:
        """Return all registered contributions."""

        return tuple(
            self._contributions.values(),
        )

    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return template directories."""

        return tuple(
            self._contributions,
        )
