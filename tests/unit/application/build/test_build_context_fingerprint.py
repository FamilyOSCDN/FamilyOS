from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildEffectiveConfiguration,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_context_fingerprint import (
    BuildContextFingerprint,
)
from familyos_cli.application.build.build_context_fingerprinter import (
    BuildContextFingerprinter,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)


def _context() -> BuildContext:
    return BuildContext(
        build_id=BuildId.generate(),
        source_state=SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
        dependency_state=DependencyState(
            declaration_path=Path("/project/pyproject.toml"),
            declaration_digest="a" * 64,
            lock_path=Path("/project/requirements.txt"),
            lock_digest="b" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(
                ToolchainVersion(distribution="build", version="1.3.0"),
                ToolchainVersion(distribution="pip-tools", version="7.5.0"),
            ),
        ),
        environment_state=EnvironmentState(
            operating_system="Linux",
            operating_system_release="6.8",
            machine_architecture="x86_64",
            virtual_environment_active=True,
            temporary_directory="/tmp/one",
            filesystem_encoding="utf-8",
        ),
        profile=BuildProfile.CI,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        output_dir=Path("/project/dist"),
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=True,
        ),
        evidence_output=None,
    )


def test_fingerprint_is_deterministic() -> None:
    fingerprinter = BuildContextFingerprinter()
    context = _context()

    first = fingerprinter.fingerprint(context)
    second = fingerprinter.fingerprint(context)

    assert first == second
    assert first.algorithm == "sha256"
    assert len(first.digest) == 64


def test_build_id_does_not_change_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(first, build_id=BuildId.generate())

    assert fingerprinter.fingerprint(first) == fingerprinter.fingerprint(second)


def test_output_paths_do_not_change_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        output_dir=Path("/different/dist"),
        evidence_output=Path("/different/evidence.json"),
    )

    assert fingerprinter.fingerprint(first) == fingerprinter.fingerprint(second)


def test_temporary_directory_does_not_change_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        environment_state=replace(
            first.environment_state,
            temporary_directory="/another/tmp",
        ),
    )

    assert fingerprinter.fingerprint(first) == fingerprinter.fingerprint(second)


def test_virtual_environment_state_does_not_change_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        environment_state=replace(
            first.environment_state,
            virtual_environment_active=False,
        ),
    )

    assert fingerprinter.fingerprint(first) == fingerprinter.fingerprint(second)


def test_dependency_digest_changes_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        dependency_state=replace(
            first.dependency_state,
            lock_digest="c" * 64,
        ),
    )

    assert fingerprinter.fingerprint(first) != fingerprinter.fingerprint(second)


def test_source_revision_changes_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        source_state=replace(first.source_state, revision="f" * 40),
    )

    assert fingerprinter.fingerprint(first) != fingerprinter.fingerprint(second)


def test_runtime_version_changes_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(first, runtime_version="3.13.8")

    assert fingerprinter.fingerprint(first) != fingerprinter.fingerprint(second)


def test_environment_architecture_changes_fingerprint() -> None:
    fingerprinter = BuildContextFingerprinter()
    first = _context()
    second = replace(
        first,
        environment_state=replace(
            first.environment_state,
            machine_architecture="arm64",
        ),
    )

    assert fingerprinter.fingerprint(first) != fingerprinter.fingerprint(second)


def test_missing_source_revision_cannot_be_fingerprinted() -> None:
    context = replace(
        _context(),
        source_state=SourceState(revision=None, dirty=False),
    )

    with pytest.raises(
        ValueError,
        match="requires a captured source revision",
    ):
        BuildContextFingerprinter().fingerprint(context)


@pytest.mark.parametrize(
    ("algorithm", "digest"),
    [
        ("sha512", "a" * 64),
        ("sha256", "a" * 63),
        ("sha256", "g" * 64),
        ("sha256", "A" * 64),
    ],
)
def test_fingerprint_rejects_noncanonical_identity(
    algorithm: str,
    digest: str,
) -> None:
    with pytest.raises(ValueError):
        BuildContextFingerprint(
            algorithm=algorithm,
            digest=digest,
        )


def test_equivalent_context_fingerprints_match() -> None:
    fingerprinter = BuildContextFingerprinter()

    first = fingerprinter.fingerprint(_context())
    second = fingerprinter.fingerprint(_context())

    assert first.matches(second)
    assert second.matches(first)


def test_different_context_fingerprints_do_not_match() -> None:
    fingerprinter = BuildContextFingerprinter()
    first_context = _context()
    second_context = replace(
        first_context,
        runtime_version="3.13.8",
    )

    first = fingerprinter.fingerprint(first_context)
    second = fingerprinter.fingerprint(second_context)

    assert not first.matches(second)
    assert not second.matches(first)
