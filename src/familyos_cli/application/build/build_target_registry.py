"""Canonical registry of supported Build Framework targets."""

from __future__ import annotations

from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import BuildTarget
from familyos_cli.application.build.build_target_definition import (
    BuildTargetDefinition,
)

_FAMILYOS_CLI_PACKAGE = BuildTargetDefinition(
    target=BuildTarget.FAMILYOS_CLI_PACKAGE,
    owner="EPIC-BLD-001 / Canonical Package Build",
    required_inputs=(
        "pyproject.toml",
        "requirements.txt",
        "package source governed by pyproject.toml",
    ),
    expected_artifacts=(
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    ),
    requires_structural_validation=True,
)

_TARGETS = {
    _FAMILYOS_CLI_PACKAGE.target: _FAMILYOS_CLI_PACKAGE,
}


def get_build_target_definition(
    target: BuildTarget,
) -> BuildTargetDefinition:
    """Return the canonical definition for one supported build target."""

    try:
        return _TARGETS[target]
    except KeyError as error:
        raise ValueError(
            f"unsupported build target: {target.value}"
        ) from error
