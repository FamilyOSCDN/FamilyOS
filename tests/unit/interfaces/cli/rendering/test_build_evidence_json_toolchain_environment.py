"""Tests for toolchain and environment projection in Build Evidence JSON."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_context import BuildProfile, BuildTarget
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.interfaces.cli.rendering.build_evidence_json import (
    BuildEvidenceJsonRenderer,
)


def test_renderer_projects_toolchain_and_environment_authorities() -> None:
    build_id = BuildId(
        UUID("01234567-89ab-4cde-8f01-23456789abcd")
    )

    evidence = BuildEvidence(
        build_id=build_id,
        source_state=SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
        runtime_version="3.13.7",
        dependency_state=DependencyState(
            declaration_path=Path("/project/pyproject.toml"),
            declaration_digest="a" * 64,
            lock_path=Path("/project/requirements.txt"),
            lock_digest="b" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(
                ToolchainVersion("build", "1.5.0"),
                ToolchainVersion("pip", "25.2"),
            ),
        ),
        environment_state=EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
        ),
        effective_configuration=EffectiveBuildConfigurationView(
            profile=BuildProfile.VALIDATION,
            target=BuildTarget.FAMILYOS_CLI_PACKAGE,
            output_dir=Path("/project/dist"),
            functional_validation=False,
            evidence_output=None,
            evidence_required=False,
            target_supported=True,
        ),
        execution_observations=(),
        validation_result=BuildValidationResult(
            build_id=build_id,
            profile=BuildValidationProfile.VALIDATION,
            checks=(),
            status=BuildValidationStatus.PASSED,
        ),
        artifact_manifest=ArtifactManifest(
            build_id=build_id,
            entries=(),
        ),
        artifact_integrities=(),
    )

    payload = json.loads(
        BuildEvidenceJsonRenderer().render(evidence)
    )

    assert payload["toolchain"] == {
        "critical_versions": [
            {
                "distribution": "build",
                "version": "1.5.0",
            },
            {
                "distribution": "pip",
                "version": "25.2",
            },
        ]
    }

    assert payload["environment"] == {
        "operating_system": "Darwin",
        "operating_system_release": "24.6.0",
        "machine_architecture": "arm64",
        "virtual_environment_active": False,
        "temporary_directory": "/tmp",
        "filesystem_encoding": "utf-8",
    }
