"""Integration tests for the complete plugin ecosystem lifecycle."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscovery,
)
from familyos_cli.plugins.ecosystem.installation import (
    PluginInstaller,
)
from familyos_cli.plugins.ecosystem.pipeline import (
    PluginResolutionPipeline,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginResolver,
)
from familyos_cli.plugins.ecosystem.verification import (
    PluginVerifier,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def write_communication_manifest(
    plugin_directory: Path,
) -> None:
    """Write the canonical Communication plugin descriptor."""

    plugin_directory.mkdir(
        parents=True,
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            "id: familyos.communication\n"
            "name: FamilyOS Communication Plugin\n"
            "version: 1.0.0\n"
            "author: FamilyOS Team\n"
            "description: Test Communication plugin package.\n"
            "module: "
            "familyos_cli.plugins.builtin.communication.plugin\n"
            "class: CommunicationPlugin\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def test_plugin_identity_survives_discovery_resolution_verification_and_installation(
    tmp_path: Path,
) -> None:
    """Canonical plugin identity should survive the ecosystem pipeline."""

    plugin_directory = (
        tmp_path / "communication"
    )

    write_communication_manifest(
        plugin_directory,
    )

    repository = PluginRepository(
        name="Integration Repository",
        url=str(tmp_path),
        repository_type="local",
    )

    pipeline = PluginResolutionPipeline(
        discovery=PluginDiscovery(),
        resolver=PluginResolver(),
    )

    plan = pipeline.resolve(
        repository=repository,
        dependencies=[
            PluginDependency(
                plugin_id="familyos.communication",
            ),
        ],
    )

    assert plan.diagnostics == []
    assert len(plan.ordered_packages) == 1

    package = plan.ordered_packages[0]

    assert package.plugin_id == "familyos.communication"
    assert package.name == "familyos.communication"
    assert package.version == "1.0.0"
    assert package.identifier() == (
        "familyos.communication@1.0.0"
    )

    verification = PluginVerifier().verify(
        package,
    )

    assert verification.valid is True
    assert verification.reason == "Package verified."

    installed = PluginInstaller().install(
        package,
        str(plugin_directory),
    )

    assert installed.plugin_id == "familyos.communication"
    assert installed.name == "familyos.communication"
    assert installed.version == "1.0.0"
    assert installed.location == str(
        plugin_directory,
    )
    assert installed.identifier() == (
        "familyos.communication@1.0.0"
    )


def test_communication_plugin_activation_registers_runtime_resources() -> None:
    """Resolved plugin identity should match runtime ownership."""

    runtime = PluginRuntime()

    plugin = CommunicationPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.communication",
    )

    assert runtime.state_by_plugin_id(
        "familyos.communication",
    ) is RuntimeState.ACTIVE

    assert runtime.plugin(
        "familyos.communication",
    ) is plugin

    generation_contributions = (
        runtime.generation_contributions()
    )

    recipe_contributions = (
        runtime.generation_recipe_contributions()
    )

    template_contributions = (
        runtime.template_contributions()
    )

    assert len(generation_contributions) == 1
    assert len(recipe_contributions) == 1
    assert len(template_contributions) == 1

    assert str(
        generation_contributions[0].preset,
    ) == "communication"

    assert generation_contributions[0].recipes == (
        "communication-documentation",
    )

    assert (
        recipe_contributions[0].recipe.name
        == "communication-documentation"
    )

    assert (
        template_contributions[0]
        .template_directory
        .name
        == "templates"
    )


def test_plugin_ecosystem_lifecycle_preserves_canonical_identity(
    tmp_path: Path,
) -> None:
    """Exercise discovery through runtime activation as one lifecycle."""

    plugin_directory = (
        tmp_path / "communication"
    )

    write_communication_manifest(
        plugin_directory,
    )

    repository = PluginRepository(
        name="Integration Repository",
        url=str(tmp_path),
        repository_type="local",
    )

    plan = PluginResolutionPipeline(
        discovery=PluginDiscovery(),
        resolver=PluginResolver(),
    ).resolve(
        repository=repository,
        dependencies=[
            PluginDependency(
                plugin_id="familyos.communication",
            ),
        ],
    )

    assert plan.diagnostics == []
    assert len(plan.ordered_packages) == 1

    package = plan.ordered_packages[0]

    verification = PluginVerifier().verify(
        package,
    )

    assert verification.valid is True

    installed = PluginInstaller().install(
        package,
        str(plugin_directory),
    )

    runtime = PluginRuntime()

    runtime.activate(
        CommunicationPlugin(),
        plugin_id=installed.plugin_id,
    )

    assert package.plugin_id == "familyos.communication"
    assert installed.plugin_id == package.plugin_id

    assert runtime.state_by_plugin_id(
        installed.plugin_id,
    ) is RuntimeState.ACTIVE

    assert runtime.plugin(
        installed.plugin_id,
    ) is not None

    assert runtime.generation_contributions()
    assert runtime.generation_recipe_contributions()
    assert runtime.template_contributions()
