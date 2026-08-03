from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
)
from familyos_cli.plugins.builtin.security.validation.security_validator import (
    SecurityValidator,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)


def test_security_plugin_has_metadata() -> None:
    plugin = SecurityPlugin()

    metadata = plugin.get_metadata()

    assert metadata is not None
    assert metadata.name == "FamilyOS Security Plugin"
    assert metadata.version == "1.0.0"


def test_security_plugin_exposes_capabilities() -> None:
    plugin = SecurityPlugin()

    capabilities = plugin.capabilities()

    assert len(capabilities) == 2

    assert all(
        isinstance(
            capability,
            PluginCapability,
        )
        for capability in capabilities
    )

    assert {
        str(capability.id)
        for capability in capabilities
    } == {
        "security.policy",
        "security.validation",
    }


def test_security_plugin_exposes_contributions() -> None:
    plugin = SecurityPlugin()

    contributions = plugin.contributions()

    assert all(
        isinstance(
            contribution,
            Contribution,
        )
        for contribution in contributions
    )

    assert len(contributions) == 3


def test_security_plugin_can_create_validator() -> None:
    plugin = SecurityPlugin()

    validator = plugin.validator()

    assert isinstance(
        validator,
        SecurityValidator,
    )
