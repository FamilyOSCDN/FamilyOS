"""Integration tests for the complete plugin ecosystem lifecycle."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
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
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    name: str,
    module: str,
    plugin_class: str,
) -> None:
    """Write a canonical plugin descriptor."""

    plugin_directory.mkdir(
        parents=True,
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            f"id: {plugin_id}\n"
            f"name: {name}\n"
            "version: 1.0.0\n"
            "author: FamilyOS Team\n"
            "description: Integration test plugin package.\n"
            f"module: {module}\n"
            f"class: {plugin_class}\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def write_communication_manifest(
    plugin_directory: Path,
) -> None:
    """Write the canonical Communication plugin descriptor."""

    write_plugin_manifest(
        plugin_directory,
        plugin_id="familyos.communication",
        name="FamilyOS Communication Plugin",
        module=(
            "familyos_cli.plugins.builtin.communication.plugin"
        ),
        plugin_class="CommunicationPlugin",
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


def test_multiple_plugins_survive_complete_ecosystem_lifecycle(
    tmp_path: Path,
) -> None:
    """Multiple official plugins should compose through one ecosystem flow."""

    write_plugin_manifest(
        tmp_path / "security",
        plugin_id="familyos.security",
        name="FamilyOS Security Plugin",
        module="familyos_cli.plugins.builtin.security.plugin",
        plugin_class="SecurityPlugin",
    )

    write_plugin_manifest(
        tmp_path / "documents",
        plugin_id="familyos.documents",
        name="FamilyOS Documents Plugin",
        module="familyos_cli.plugins.builtin.documents.plugin",
        plugin_class="DocumentsPlugin",
    )

    write_plugin_manifest(
        tmp_path / "communication",
        plugin_id="familyos.communication",
        name="FamilyOS Communication Plugin",
        module=(
            "familyos_cli.plugins.builtin.communication.plugin"
        ),
        plugin_class="CommunicationPlugin",
    )

    repository = PluginRepository(
        name="Integration Repository",
        url=str(tmp_path),
        repository_type="local",
    )

    requested_plugin_ids = [
        "familyos.security",
        "familyos.documents",
        "familyos.communication",
    ]

    plan = PluginResolutionPipeline(
        discovery=PluginDiscovery(),
        resolver=PluginResolver(),
    ).resolve(
        repository=repository,
        dependencies=[
            PluginDependency(
                plugin_id=plugin_id,
            )
            for plugin_id in requested_plugin_ids
        ],
    )

    assert plan.diagnostics == []
    assert plan.skipped_packages == []

    assert [
        package.plugin_id
        for package in plan.ordered_packages
    ] == requested_plugin_ids

    verifier = PluginVerifier()
    installer = PluginInstaller()

    installed_plugins = []

    for package in plan.ordered_packages:
        verification = verifier.verify(
            package,
        )

        assert verification.valid is True

        installed_plugins.append(
            installer.install(
                package,
                str(
                    tmp_path
                    / package.plugin_id.removeprefix(
                        "familyos.",
                    )
                ),
            ),
        )

    assert [
        installed.plugin_id
        for installed in installed_plugins
    ] == requested_plugin_ids

    runtime = PluginRuntime()

    runtime_plugins = {
        "familyos.security": SecurityPlugin(),
        "familyos.documents": DocumentsPlugin(),
        "familyos.communication": CommunicationPlugin(),
    }

    for installed in installed_plugins:
        runtime.activate(
            runtime_plugins[
                installed.plugin_id
            ],
            plugin_id=installed.plugin_id,
        )

    for plugin_id in requested_plugin_ids:
        assert runtime.state_by_plugin_id(
            plugin_id,
        ) is RuntimeState.ACTIVE

        assert runtime.plugin(
            plugin_id,
        ) is runtime_plugins[
            plugin_id
        ]

    generation_contributions = (
        runtime.generation_contributions()
    )

    recipe_contributions = (
        runtime.generation_recipe_contributions()
    )

    template_contributions = (
        runtime.template_contributions()
    )

    assert len(generation_contributions) == 3
    assert len(recipe_contributions) == 3
    assert len(template_contributions) == 3

    assert {
        str(contribution.preset)
        for contribution in generation_contributions
    } == {
        "security",
        "documents",
        "communication",
    }

    assert {
        contribution.recipe.name
        for contribution in recipe_contributions
    } == {
        "security_documentation",
        "documents-documentation",
        "communication-documentation",
    }

    contribution_ids = {
        contribution.id.value
        for contribution in (
            *generation_contributions,
            *recipe_contributions,
            *template_contributions,
        )
    }

    assert any(
        contribution_id.startswith(
            "familyos.security.",
        )
        for contribution_id in contribution_ids
    )

    assert any(
        contribution_id.startswith(
            "familyos.documents.",
        )
        for contribution_id in contribution_ids
    )

    assert any(
        contribution_id.startswith(
            "familyos.communication.",
        )
        for contribution_id in contribution_ids
    )
