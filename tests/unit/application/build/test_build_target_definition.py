"""Tests for canonical Build Target definitions."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import BuildTarget
from familyos_cli.application.build.build_target_definition import (
    BuildTargetDefinition,
)
from familyos_cli.application.build.build_target_registry import (
    get_build_target_definition,
)
from familyos_cli.application.build.discover_package_artifacts import (
    PACKAGE_ARTIFACT_DEFINITIONS,
)


def test_familyos_cli_package_target_is_canonical() -> None:
    definition = get_build_target_definition(
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    assert definition.target is BuildTarget.FAMILYOS_CLI_PACKAGE
    assert definition.owner == "EPIC-BLD-001 / Canonical Package Build"
    assert definition.required_inputs == (
        "pyproject.toml",
        "requirements.txt",
        "package source governed by pyproject.toml",
    )
    assert definition.expected_artifacts == (
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )
    assert definition.requires_structural_validation is True


def test_familyos_cli_target_matches_package_discovery_contract() -> None:
    definition = get_build_target_definition(
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    discovered_artifact_classes = tuple(
        artifact_definition.artifact_class
        for artifact_definition in PACKAGE_ARTIFACT_DEFINITIONS
    )

    assert discovered_artifact_classes == definition.expected_artifacts


def test_target_definition_is_immutable() -> None:
    definition = get_build_target_definition(
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    with pytest.raises(FrozenInstanceError):
        definition.owner = "other-owner"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("owner", "required_inputs", "expected_artifacts", "message"),
    (
        (
            "",
            ("pyproject.toml",),
            (ArtifactClass.PYTHON_WHEEL,),
            "build target owner must not be empty",
        ),
        (
            "EPIC-BLD-001",
            (),
            (ArtifactClass.PYTHON_WHEEL,),
            "build target must define required inputs",
        ),
        (
            "EPIC-BLD-001",
            ("pyproject.toml",),
            (),
            "build target must define expected artifacts",
        ),
    ),
)
def test_target_definition_rejects_incomplete_contract(
    owner: str,
    required_inputs: tuple[str, ...],
    expected_artifacts: tuple[ArtifactClass, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        BuildTargetDefinition(
            target=BuildTarget.FAMILYOS_CLI_PACKAGE,
            owner=owner,
            required_inputs=required_inputs,
            expected_artifacts=expected_artifacts,
            requires_structural_validation=True,
        )
