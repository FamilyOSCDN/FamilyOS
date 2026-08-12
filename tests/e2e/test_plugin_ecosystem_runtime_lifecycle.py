"""End-to-end tests for the plugin ecosystem runtime lifecycle."""

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
from familyos_cli.plugins.plugin_manager import (
    PluginManager,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def write_communication_manifest(
    plugin_directory: Path,
) -> None:
    """Write a canonical Communication plugin descriptor."""

    plugin_directory.mkdir(
        parents=True,
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            "id: familyos.communication\n"
            "name: FamilyOS Communication Plugin\n"
            "version: 1.0.0\n"
            "author: FamilyOS Team\n"
            "description: End-to-end Communication plugin package.\n"
            "module: familyos_cli.plugins.builtin.communication.plugin\n"
            "class: CommunicationPlugin\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def test_plugin_ecosystem_reaches_runtime_through_dynamic_loading(
    tmp_path: Path,
) -> None:
    """Exercise the complete ecosystem-to-runtime plugin lifecycle."""

    plugin_directory = tmp_path / "communication"

    write_communication_manifest(
        plugin_directory,
    )

    repository = PluginRepository(
        name="E2E Repository",
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
    assert plan.skipped_packages == []
    assert len(plan.ordered_packages) == 1

    package = plan.ordered_packages[0]

    assert package.plugin_id == "familyos.communication"
    assert package.version == "1.0.0"

    verification = PluginVerifier().verify(
        package,
    )

    assert verification.valid is True

    installed = PluginInstaller().install(
        package,
        str(plugin_directory),
    )

    assert installed.plugin_id == package.plugin_id
    assert installed.version == package.version
    assert installed.location == str(plugin_directory)

    manager = PluginManager(
        plugins_directory=tmp_path,
    )

    manager.load_all()

    runtime = manager.runtime()

    plugin = runtime.plugin(
        installed.plugin_id,
    )

    assert isinstance(
        plugin,
        CommunicationPlugin,
    )

    assert runtime.state_by_plugin_id(
        installed.plugin_id,
    ) is RuntimeState.ACTIVE

    assert manager.get(
        installed.plugin_id,
    ) is not None

    capabilities = (
        runtime.capabilities().list()
    )

    assert {
        str(capability.id)
        for capability in capabilities
    } == {
        "familyos.communication.messaging",
        "familyos.communication.archive",
    }

    assert all(
        str(capability.id).startswith(
            f"{installed.plugin_id}.",
        )
        for capability in capabilities
    )

    generation_contributions = (
        runtime.generation_contributions()
    )

    recipe_contributions = (
        runtime.generation_recipe_contributions()
    )

    template_contributions = (
        runtime.template_contributions()
    )

    assert generation_contributions
    assert recipe_contributions
    assert template_contributions

    assert all(
        contribution.id.value.startswith(
            f"{installed.plugin_id}.",
        )
        for contribution in (
            *generation_contributions,
            *recipe_contributions,
            *template_contributions,
        )
    )

    assert tuple(
        observation.new_state
        for observation in (
            runtime.context().observations.for_plugin(
                installed.plugin_id,
            )
        )
    ) == (
        RuntimeState.INITIALIZED,
        RuntimeState.ACTIVE,
    )

    manager.deactivate(
        installed.plugin_id,
    )

    assert runtime.state_by_plugin_id(
        installed.plugin_id,
    ) is RuntimeState.STOPPED

    assert runtime.plugins().all() == []
    assert runtime.capabilities().list() == ()

    assert runtime.generation_contributions() == ()
    assert runtime.generation_recipe_contributions() == ()
    assert runtime.template_contributions() == ()

    assert tuple(
        observation.new_state
        for observation in (
            runtime.context().observations.for_plugin(
                installed.plugin_id,
            )
        )
    ) == (
        RuntimeState.INITIALIZED,
        RuntimeState.ACTIVE,
        RuntimeState.STOPPING,
        RuntimeState.STOPPED,
    )
