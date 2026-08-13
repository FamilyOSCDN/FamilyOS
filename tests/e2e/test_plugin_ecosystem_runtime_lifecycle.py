"""End-to-end tests for the plugin ecosystem runtime lifecycle."""

from __future__ import annotations

from pathlib import Path

from pytest import raises

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
)
from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)
from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
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
from familyos_cli.plugins.plugin import (
    Plugin,
)
from familyos_cli.plugins.plugin_manager import (
    PluginManager,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)

OFFICIAL_PLUGINS: tuple[
    tuple[str, str, str, type[Plugin]],
    ...,
] = (
    (
        "familyos.communication",
        "familyos_cli.plugins.builtin.communication.plugin",
        "CommunicationPlugin",
        CommunicationPlugin,
    ),
    (
        "familyos.documents",
        "familyos_cli.plugins.builtin.documents.plugin",
        "DocumentsPlugin",
        DocumentsPlugin,
    ),
    (
        "familyos.education",
        "familyos_cli.plugins.builtin.education.plugin",
        "EducationPlugin",
        EducationPlugin,
    ),
    (
        "familyos.finance",
        "familyos_cli.plugins.builtin.finance.plugin",
        "FinancePlugin",
        FinancePlugin,
    ),
    (
        "familyos.health",
        "familyos_cli.plugins.builtin.health.plugin",
        "HealthPlugin",
        HealthPlugin,
    ),
    (
        "familyos.security",
        "familyos_cli.plugins.builtin.security.plugin",
        "SecurityPlugin",
        SecurityPlugin,
    ),
)


EXPECTED_CAPABILITY_IDS = {
    "familyos.communication.messaging",
    "familyos.communication.archive",
    "familyos.documents.document",
    "familyos.documents.archive",
    "familyos.education.learner",
    "familyos.education.course",
    "familyos.education.record",
    "familyos.finance.account",
    "familyos.finance.transaction",
    "familyos.finance.asset",
    "familyos.finance.liability",
    "familyos.finance.budget",
    "familyos.health.profile",
    "familyos.health.record",
    "familyos.security.policy",
    "familyos.security.validation",
}


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    module: str,
    plugin_class: str,
) -> None:
    """Write a canonical official plugin descriptor."""

    plugin_directory.mkdir(
        parents=True,
    )

    plugin_name = plugin_id.removeprefix(
        "familyos.",
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            f"id: {plugin_id}\n"
            f"name: FamilyOS {plugin_name.title()} Plugin\n"
            "version: 1.0.0\n"
            "author: FamilyOS Team\n"
            f"description: End-to-end {plugin_name} plugin package.\n"
            f"module: {module}\n"
            f"class: {plugin_class}\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def prepare_official_plugin_repository(
    root: Path,
) -> None:
    """Create manifests for all official plugins."""

    for (
        plugin_id,
        module,
        plugin_class,
        _,
    ) in OFFICIAL_PLUGINS:
        plugin_directory = (
            root
            / plugin_id.removeprefix(
                "familyos.",
            )
        )

        write_plugin_manifest(
            plugin_directory,
            plugin_id=plugin_id,
            module=module,
            plugin_class=plugin_class,
        )


def test_plugin_ecosystem_reaches_runtime_through_dynamic_loading(
    tmp_path: Path,
) -> None:
    """Exercise the complete ecosystem-to-runtime plugin lifecycle."""

    plugin_directory = tmp_path / "communication"

    write_plugin_manifest(
        plugin_directory,
        plugin_id="familyos.communication",
        module="familyos_cli.plugins.builtin.communication.plugin",
        plugin_class="CommunicationPlugin",
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

    capabilities = runtime.capabilities().list()

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


def test_all_official_plugins_share_runtime_without_identity_collisions(
    tmp_path: Path,
) -> None:
    """Exercise all official plugins in one shared runtime."""

    prepare_official_plugin_repository(
        tmp_path,
    )

    manager = PluginManager(
        plugins_directory=tmp_path,
    )

    manager.load_all()

    runtime = manager.runtime()

    expected_plugin_ids = {
        plugin_id
        for (
            plugin_id,
            _,
            _,
            _,
        ) in OFFICIAL_PLUGINS
    }

    assert {
        descriptor.id
        for descriptor in manager.list_plugins()
    } == expected_plugin_ids

    assert len(
        runtime.plugins().all(),
    ) == len(
        OFFICIAL_PLUGINS,
    )

    for (
        plugin_id,
        _,
        _,
        expected_type,
    ) in OFFICIAL_PLUGINS:
        assert isinstance(
            runtime.plugin(
                plugin_id,
            ),
            expected_type,
        )

        assert runtime.state_by_plugin_id(
            plugin_id,
        ) is RuntimeState.ACTIVE

        assert manager.get(
            plugin_id,
        ) is not None

        assert tuple(
            observation.new_state
            for observation in (
                runtime.context().observations.for_plugin(
                    plugin_id,
                )
            )
        ) == (
            RuntimeState.INITIALIZED,
            RuntimeState.ACTIVE,
        )

    capabilities = runtime.capabilities().list()

    capability_ids = {
        str(capability.id)
        for capability in capabilities
    }

    assert capability_ids == EXPECTED_CAPABILITY_IDS

    assert len(
        capability_ids,
    ) == len(
        capabilities,
    )

    for plugin_id in expected_plugin_ids:
        assert any(
            capability_id.startswith(
                f"{plugin_id}.",
            )
            for capability_id in capability_ids
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

    all_contributions = (
        *generation_contributions,
        *recipe_contributions,
        *template_contributions,
    )

    contribution_ids = [
        contribution.id.value
        for contribution in all_contributions
    ]

    assert len(
        contribution_ids,
    ) == len(
        set(
            contribution_ids,
        ),
    )

    for contribution_id in contribution_ids:
        assert any(
            contribution_id.startswith(
                f"{plugin_id}.",
            )
            for plugin_id in expected_plugin_ids
        )

    manager.deactivate(
        "familyos.education",
    )

    assert runtime.state_by_plugin_id(
        "familyos.education",
    ) is RuntimeState.STOPPED

    with raises(
        ValueError,
        match="Plugin 'familyos.education' is not active.",
    ):
        runtime.plugin(
            "familyos.education",
        )

    remaining_plugin_ids = (
        expected_plugin_ids
        - {
            "familyos.education",
        }
    )

    assert len(
        runtime.plugins().all(),
    ) == len(
        remaining_plugin_ids,
    )

    for plugin_id in remaining_plugin_ids:
        assert runtime.state_by_plugin_id(
            plugin_id,
        ) is RuntimeState.ACTIVE

        assert runtime.plugin(
            plugin_id,
        ) is not None

    remaining_capability_ids = {
        str(capability.id)
        for capability in (
            runtime.capabilities().list()
        )
    }

    assert not any(
        capability_id.startswith(
            "familyos.education.",
        )
        for capability_id in remaining_capability_ids
    )

    assert remaining_capability_ids == {
        capability_id
        for capability_id in EXPECTED_CAPABILITY_IDS
        if not capability_id.startswith(
            "familyos.education.",
        )
    }

    remaining_contributions = (
        *runtime.generation_contributions(),
        *runtime.generation_recipe_contributions(),
        *runtime.template_contributions(),
    )

    assert not any(
        contribution.id.value.startswith(
            "familyos.education.",
        )
        for contribution in remaining_contributions
    )

    assert tuple(
        observation.new_state
        for observation in (
            runtime.context().observations.for_plugin(
                "familyos.education",
            )
        )
    ) == (
        RuntimeState.INITIALIZED,
        RuntimeState.ACTIVE,
        RuntimeState.STOPPING,
        RuntimeState.STOPPED,
    )

    for plugin_id in remaining_plugin_ids:
        manager.deactivate(
            plugin_id,
        )

    assert runtime.plugins().all() == []
    assert runtime.capabilities().list() == ()

    assert runtime.generation_contributions() == ()
    assert runtime.generation_recipe_contributions() == ()
    assert runtime.template_contributions() == ()

    for plugin_id in expected_plugin_ids:
        assert runtime.state_by_plugin_id(
            plugin_id,
        ) is RuntimeState.STOPPED

        assert tuple(
            observation.new_state
            for observation in (
                runtime.context().observations.for_plugin(
                    plugin_id,
                )
            )
        ) == (
            RuntimeState.INITIALIZED,
            RuntimeState.ACTIVE,
            RuntimeState.STOPPING,
            RuntimeState.STOPPED,
        )
