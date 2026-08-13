"""Tests for the generation domains command."""

from __future__ import annotations

from familyos_cli.interfaces.cli.commands import (
    generation_domains as generation_domains_module,
)
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


class FakeDomainGenerationCatalogService:
    """Fake domain generation catalog used by CLI tests."""

    def list_domains(
        self,
    ) -> tuple[DomainGenerationContribution, ...]:
        """Return fake domain generation contributions."""

        return (
            DomainGenerationContribution(
                id=PluginContributionId(
                    "familyos.test.domain.health",
                ),
                domain="Health",
                description="Health domain generation.",
                artifacts=(
                    "health_documentation",
                    "health_domain_model",
                ),
            ),
        )


class FakeCommandContext:
    """Fake command context used by CLI tests."""

    def __init__(self) -> None:
        """Initialize fake context."""

        self.domain_generation_catalog = (
            FakeDomainGenerationCatalogService()
        )


def test_generation_domains_displays_available_domains(
    monkeypatch,
) -> None:
    """Display domain contributions and their artifacts."""

    messages: list[str] = []

    monkeypatch.setattr(
        generation_domains_module,
        "CommandContext",
        FakeCommandContext,
    )

    monkeypatch.setattr(
        Output,
        "info",
        messages.append,
    )

    generation_domains_module.generation_domains()

    assert messages == [
        "Available generation domains:",
        "Health",
        "  Health domain generation.",
        "  Artifacts:",
        "    - health_documentation",
        "    - health_domain_model",
    ]
