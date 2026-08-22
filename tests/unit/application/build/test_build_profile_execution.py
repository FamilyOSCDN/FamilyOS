"""Tests for canonical build-profile enforcement during execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import familyos_cli.application.build.run_package_build as run_package_build_module
from familyos_cli.application.build import (
    BuildProfile,
    BuildTarget,
    DiscoverPackageArtifactsUseCase,
    PackageBuildResult,
    PackageBuildStatus,
    RunPackageBuildUseCase,
    SourceState,
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact
from familyos_cli.application.build.package_functional_validation import (
    PythonWheelFunctionalValidationResult,
)
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort
from familyos_cli.application.ports.build.python_wheel_functional_validator import (
    PythonWheelFunctionalValidatorPort,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)


class _Builder(PackageBuilderPort):
    def __init__(self) -> None:
        self.called = False

    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        del project_root, output_dir
        self.called = True
        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="unexpected execution",
        )


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(self) -> None:
        self.called = False

    def observe(self, *, project_root: Path) -> SourceState:
        del project_root
        self.called = True
        return SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )


class _FunctionalValidator(PythonWheelFunctionalValidatorPort):
    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        raise AssertionError(
            f"functional validation must not execute: {candidate}"
        )


def test_profile_target_compatibility_is_checked_before_build_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    builder = _Builder()
    source_provider = _SourceStateProvider()

    def reject_profile_target(
        profile: BuildProfile,
        target: BuildTarget,
    ) -> Any:
        assert profile is BuildProfile.CI
        assert target is BuildTarget.FAMILYOS_CLI_PACKAGE
        raise ValueError(
            "unsupported build profile/target combination: "
            "ci/familyos-cli-package"
        )

    monkeypatch.setattr(
        run_package_build_module,
        "validate_profile_target",
        reject_profile_target,
    )

    use_case = RunPackageBuildUseCase(
        builder=builder,
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(tmp_path),
        functional_validator=_FunctionalValidator(),
        source_state_provider=source_provider,
        project_root=tmp_path,
    )

    with pytest.raises(
        ValueError,
        match="unsupported build profile/target combination",
    ):
        use_case.execute(
            Path("dist"),
            profile=BuildProfile.CI,
            target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        )

    assert source_provider.called is False
    assert builder.called is False


@pytest.mark.parametrize("profile", tuple(BuildProfile))
def test_current_profiles_are_accepted_for_familyos_cli_target(
    profile: BuildProfile,
) -> None:
    from familyos_cli.application.build.build_profile_registry import (
        validate_profile_target,
    )

    definition = validate_profile_target(
        profile,
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    assert definition.profile is profile
