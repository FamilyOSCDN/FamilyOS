"""Coherent acceptance matrix for canonical build-configuration resolution."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from inspect import signature
from pathlib import Path
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_context_resolver import (
    BuildContextResolver,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_profile_registry import (
    get_build_profile_definition,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.effective_configuration_validation import (
    EffectiveConfigurationValidationResult,
)
from familyos_cli.application.build.effective_configuration_validator import (
    EffectiveConfigurationValidator,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.repository_layout import RepositoryLayout
from familyos_cli.application.build.repository_layout_validator import (
    RepositoryLayoutValidator,
)
from familyos_cli.application.build.run_package_build import RunPackageBuildUseCase
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)
from familyos_cli.interfaces.cli.commands.build import DEFAULT_OUTPUT_DIR, build

_BUILD_ID = BuildId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_OTHER_BUILD_ID = BuildId(UUID("11234567-89ab-4cde-8f01-23456789abcd"))

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)

_TOOLCHAIN_STATE = ToolchainState(
    critical_versions=(ToolchainVersion("build", "1.5.0"),),
)

_ENVIRONMENT_STATE = EnvironmentState(
    operating_system="TestOS",
    operating_system_release="1.0",
    machine_architecture="test-machine",
)


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(self, state: SourceState) -> None:
        self._state = state

    def observe(self, *, project_root: Path) -> SourceState:
        return self._state


class _DependencyStateProvider(DependencyStateProvider):
    def __init__(self, state: DependencyState) -> None:
        self._state = state

    def capture(self, *, project_root: Path) -> DependencyState:
        return self._state


class _ToolchainStateProvider(ToolchainStateProvider):
    def __init__(self, state: ToolchainState) -> None:
        self._state = state

    def capture(self) -> ToolchainState:
        return self._state


class _EnvironmentStateProvider(EnvironmentStateProvider):
    def __init__(self, state: EnvironmentState) -> None:
        self._state = state

    def capture(self) -> EnvironmentState:
        return self._state


def _dependency_state(
    project_root: Path,
    *,
    declaration_digest: str = "a" * 64,
    lock_digest: str = "b" * 64,
) -> DependencyState:
    return DependencyState(
        declaration_path=project_root / "pyproject.toml",
        declaration_digest=declaration_digest,
        lock_path=project_root / "requirements.txt",
        lock_digest=lock_digest,
    )


def _resolve(
    project_root: Path,
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    profile: BuildProfile = BuildProfile.DEVELOPMENT,
    target: BuildTarget = BuildTarget.FAMILYOS_CLI_PACKAGE,
    functional_validation: bool = False,
    evidence_output: Path | None = None,
    build_id: BuildId = _BUILD_ID,
    source_state: SourceState = _SOURCE_STATE,
    dependency_state: DependencyState | None = None,
    toolchain_state: ToolchainState = _TOOLCHAIN_STATE,
    environment_state: EnvironmentState = _ENVIRONMENT_STATE,
    runtime_version: str = "3.13.7",
) -> BuildContext:
    dependency = dependency_state or _dependency_state(project_root)

    return BuildContextResolver(
        _SourceStateProvider(source_state),
        project_root,
        _DependencyStateProvider(dependency),
        _ToolchainStateProvider(toolchain_state),
        _EnvironmentStateProvider(environment_state),
    ).resolve(
        output_dir,
        build_id=build_id,
        profile=profile,
        target=target,
        functional_validation=functional_validation,
        evidence_output=evidence_output,
        runtime_version=runtime_version,
    )


def _view(context: BuildContext) -> EffectiveBuildConfigurationView:
    return EffectiveBuildConfigurationView.from_context(
        context,
        get_build_profile_definition(context.profile),
    )


def _validate(
    context: BuildContext,
) -> EffectiveConfigurationValidationResult:
    layout = RepositoryLayout.from_project_root(
        context.output_dir.parent,
    )
    layout_validator = RepositoryLayoutValidator()

    return EffectiveConfigurationValidator().validate(
        context=context,
        profile_definition=get_build_profile_definition(context.profile),
        output_layout_validation=layout_validator.validate_output_dir(
            layout=layout,
            output_dir=context.output_dir,
        ),
        evidence_layout_validation=layout_validator.validate_evidence_output(
            layout=layout,
            evidence_output=context.evidence_output,
            package_output_dir=context.output_dir,
        ),
    )


def test_public_invocation_defaults_match_canonical_defaults(
    tmp_path: Path,
) -> None:
    use_case_parameters = signature(
        RunPackageBuildUseCase.execute,
    ).parameters
    cli_parameters = signature(build).parameters
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert (
        use_case_parameters["profile"].default
        is BuildProfile.DEVELOPMENT
    )
    assert (
        use_case_parameters["target"].default
        is BuildTarget.FAMILYOS_CLI_PACKAGE
    )
    assert use_case_parameters["validate_functionally"].default is False
    assert use_case_parameters["evidence_output"].default is None
    assert cli_parameters["output_dir"].default == DEFAULT_OUTPUT_DIR
    assert layout.default_output_dir == tmp_path / DEFAULT_OUTPUT_DIR


def test_default_and_explicit_development_inputs_resolve_equivalently(
    tmp_path: Path,
) -> None:
    default_view = _view(_resolve(tmp_path))
    explicit_view = _view(
        _resolve(
            tmp_path,
            output_dir=Path("dist"),
            profile=BuildProfile.DEVELOPMENT,
            target=BuildTarget.FAMILYOS_CLI_PACKAGE,
            functional_validation=False,
            evidence_output=None,
        )
    )

    assert default_view == explicit_view
    assert default_view.output_dir == (tmp_path / "dist").resolve()
    assert default_view.evidence_requested is False


def test_explicit_overrides_are_inspectable(tmp_path: Path) -> None:
    context = _resolve(
        tmp_path,
        output_dir=Path("packages"),
        profile=BuildProfile.RELEASE_CANDIDATE,
        functional_validation=True,
        evidence_output=Path("evidence/release.json"),
    )

    view = _view(context)

    assert view.profile is BuildProfile.RELEASE_CANDIDATE
    assert view.target is BuildTarget.FAMILYOS_CLI_PACKAGE
    assert view.output_dir == (tmp_path / "packages").resolve()
    assert view.functional_validation is True
    assert view.evidence_output == (
        tmp_path / "evidence/release.json"
    ).resolve()
    assert view.evidence_requested is True
    assert view.evidence_required is True
    assert view.target_supported is True


def test_equivalent_path_forms_resolve_to_equivalent_configuration(
    tmp_path: Path,
) -> None:
    relative = _view(
        _resolve(
            tmp_path,
            output_dir=Path("generated/../dist"),
            evidence_output=Path("reports/../build-evidence.json"),
        )
    )
    absolute = _view(
        _resolve(
            tmp_path,
            output_dir=(tmp_path / "dist").resolve(),
            evidence_output=(tmp_path / "build-evidence.json").resolve(),
        )
    )

    assert relative == absolute


@pytest.mark.parametrize(
    ("profile", "evidence_required"),
    (
        (BuildProfile.DEVELOPMENT, False),
        (BuildProfile.VALIDATION, False),
        (BuildProfile.CI, True),
        (BuildProfile.RELEASE_CANDIDATE, True),
    ),
)
def test_profile_evidence_policy_is_inspectable(
    tmp_path: Path,
    profile: BuildProfile,
    evidence_required: bool,
) -> None:
    evidence_output = (
        Path("build-evidence.json") if evidence_required else None
    )
    context = _resolve(
        tmp_path,
        profile=profile,
        evidence_output=evidence_output,
    )

    view = _view(context)

    assert view.evidence_required is evidence_required
    assert view.evidence_requested is evidence_required
    assert _validate(context).successful is True


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_required_evidence_conflict_is_deterministic(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    context = _resolve(tmp_path, profile=profile)

    first = _validate(context)
    second = _validate(context)

    assert first == second
    assert first.successful is False
    assert first.diagnostic == (
        f"build profile requires an evidence output: {profile.value}"
    )


def test_unsupported_profile_target_conflict_is_inspectable(
    tmp_path: Path,
) -> None:
    context = _resolve(tmp_path)
    definition = replace(
        get_build_profile_definition(BuildProfile.DEVELOPMENT),
        supported_targets=cast(tuple[BuildTarget, ...], ("unsupported",)),
    )
    view = EffectiveBuildConfigurationView.from_context(context, definition)

    assert view.target_supported is False


@pytest.mark.parametrize(
    "evidence_output",
    (Path("pyproject.toml"), Path("requirements.txt"), Path("src/report.json")),
)
def test_authoritative_evidence_path_conflicts_are_rejected(
    tmp_path: Path,
    evidence_output: Path,
) -> None:
    context = _resolve(tmp_path, evidence_output=evidence_output)

    result = _validate(context)

    assert result.successful is False
    assert result.findings[-1].component == "evidence-output"


def test_evidence_and_package_output_overlap_is_rejected(
    tmp_path: Path,
) -> None:
    context = _resolve(
        tmp_path,
        output_dir=Path("dist"),
        evidence_output=Path("dist/build-evidence.json"),
    )

    result = _validate(context)

    assert result.successful is False
    assert result.diagnostic == (
        "build evidence output must not overlap package output directory"
    )


def test_relative_resolution_is_independent_of_working_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    first_caller = tmp_path / "first-caller"
    second_caller = tmp_path / "second-caller"
    first_caller.mkdir()
    second_caller.mkdir()

    monkeypatch.chdir(first_caller)
    first = _view(
        _resolve(
            project_root,
            evidence_output=Path("build-evidence.json"),
        )
    )

    monkeypatch.chdir(second_caller)
    second = _view(
        _resolve(
            project_root,
            evidence_output=Path("build-evidence.json"),
        )
    )

    assert first == second


def test_repeated_resolution_is_deterministic(tmp_path: Path) -> None:
    first = _view(_resolve(tmp_path, functional_validation=True))
    second = _view(_resolve(tmp_path, functional_validation=True))

    assert first == second


def test_observed_state_differences_do_not_change_configuration_projection(
    tmp_path: Path,
) -> None:
    first_context = _resolve(tmp_path)
    second_context = _resolve(
        tmp_path,
        build_id=_OTHER_BUILD_ID,
        source_state=SourceState(revision="f" * 40, dirty=True),
        dependency_state=_dependency_state(
            tmp_path,
            declaration_digest="c" * 64,
            lock_digest="d" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(ToolchainVersion("build", "9.9.9"),),
        ),
        environment_state=EnvironmentState(
            operating_system="OtherOS",
            operating_system_release="2.0",
            machine_architecture="other-machine",
            temporary_directory="/different-temp",
        ),
        runtime_version="3.13.99",
    )

    assert first_context != second_context
    assert first_context.source_state != second_context.source_state
    assert first_context.dependency_state != second_context.dependency_state
    assert first_context.toolchain_state != second_context.toolchain_state
    assert first_context.environment_state != second_context.environment_state
    assert first_context.runtime_version != second_context.runtime_version
    assert _view(first_context) == _view(second_context)


def test_projection_has_closed_non_sensitive_surface(tmp_path: Path) -> None:
    view = _view(_resolve(tmp_path))

    assert tuple(field.name for field in fields(view)) == (
        "profile",
        "target",
        "output_dir",
        "functional_validation",
        "evidence_output",
        "evidence_required",
        "target_supported",
    )
    assert "token" not in repr(view).lower()
    assert "credential" not in repr(view).lower()
    assert "environment" not in repr(view).lower()


def test_projection_is_immutable(tmp_path: Path) -> None:
    view = _view(_resolve(tmp_path))

    with pytest.raises(FrozenInstanceError):
        view.evidence_required = True  # type: ignore[misc]


def test_projection_rejects_mismatched_profile_policy(tmp_path: Path) -> None:
    context = _resolve(tmp_path)

    with pytest.raises(
        ValueError,
        match="resolved build profile does not match inspection policy",
    ):
        EffectiveBuildConfigurationView.from_context(
            context,
            get_build_profile_definition(BuildProfile.CI),
        )


@pytest.mark.parametrize(
    ("enum_type", "value"),
    ((BuildProfile, "unknown"), (BuildTarget, "unknown")),
)
def test_unknown_profile_and_target_values_remain_rejected(
    enum_type: type[BuildProfile] | type[BuildTarget],
    value: str,
) -> None:
    with pytest.raises(ValueError):
        enum_type(value)
