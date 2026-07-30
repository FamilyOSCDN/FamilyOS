from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


class HealthPlugin(Plugin):
    """Test health plugin."""

    def domain_contribution(
        self,
    ) -> DomainGenerationContribution:
        """Return domain generation contribution."""

        return DomainGenerationContribution(
            domain="Health",
            description="Health domain generation.",
            artifacts=(
                "health_documentation",
                "health_domain_model",
            ),
        )


def test_plugin_runtime_registers_domain_generation_contribution() -> None:
    runtime = PluginRuntime()

    plugin = HealthPlugin()

    runtime.activate(
        plugin,
    )

    contributions = (
        runtime.domain_generation_contributions()
    )

    assert contributions == (
        DomainGenerationContribution(
            domain="Health",
            description="Health domain generation.",
            artifacts=(
                "health_documentation",
                "health_domain_model",
            ),
        ),
    )
