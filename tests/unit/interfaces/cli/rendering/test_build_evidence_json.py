"""Tests for canonical Build Evidence JSON rendering."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from uuid import UUID

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
    ArtifactIntegrity,
)
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifest,
    ArtifactManifestEntry,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import BuildProfile, BuildTarget
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
    BuildValidationDomain,
    BuildValidationProfile,
    BuildValidationRequirement,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.package_validation import (
    PackageStructuralValidationStatus,
)
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.interfaces.cli.rendering.build_evidence_json import (
    BuildEvidenceJsonRenderer,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_SOURCE_STATE = SourceState(
    revision="a" * 40,
    dirty=False,
)

_DEPENDENCY_STATE = DependencyState(
    declaration_path=Path("/checkout/pyproject.toml"),
    declaration_digest="c" * 64,
    lock_path=Path("/checkout/requirements.txt"),
    lock_digest="d" * 64,
)

_ARTIFACT_PATH = Path(
    "dist/familyos_cli-0.1.0-py3-none-any.whl"
)

_IDENTITY = ArtifactIdentity(
    build_id=_BUILD_ID,
    source_revision=_SOURCE_STATE.revision,
    logical_name="familyos-cli",
    artifact_type=ArtifactClass.PYTHON_WHEEL,
    version="0.1.0",
    size=1024,
    path=_ARTIFACT_PATH,
)

_INTEGRITY = ArtifactIntegrity(
    artifact_identity=_IDENTITY,
    algorithm=ArtifactDigestAlgorithm.SHA256,
    digest="b" * 64,
)

_MANIFEST = ArtifactManifest(
    build_id=_BUILD_ID,
    entries=(
        ArtifactManifestEntry(
            logical_name="familyos-cli",
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            version="0.1.0",
            size=1024,
            path=_ARTIFACT_PATH,
            digest_algorithm=ArtifactDigestAlgorithm.SHA256,
            digest="b" * 64,
            structural_validation_status=(
                PackageStructuralValidationStatus.VALID
            ),
        ),
    ),
)

_VALIDATION = BuildValidationResult(
    build_id=_BUILD_ID,
    profile=BuildValidationProfile.CI,
    checks=(
        BuildValidationCheckResult(
            check_id="artifact-integrity",
            domain=BuildValidationDomain.INTEGRITY,
            requirement=BuildValidationRequirement.REQUIRED,
            status=BuildValidationStatus.PASSED,
        ),
    ),
    status=BuildValidationStatus.PASSED,
)

_EFFECTIVE_CONFIGURATION = EffectiveBuildConfigurationView(
    profile=BuildProfile.CI,
    target=BuildTarget.FAMILYOS_CLI_PACKAGE,
    output_dir=Path("/checkout/dist"),
    functional_validation=False,
    evidence_output=Path("/checkout/build-evidence.json"),
    evidence_required=True,
    target_supported=True,
)

_EVIDENCE = BuildEvidence(
    build_id=_BUILD_ID,
    source_state=_SOURCE_STATE,
    dependency_state=_DEPENDENCY_STATE,
    effective_configuration=_EFFECTIVE_CONFIGURATION,
    validation_result=_VALIDATION,
    artifact_manifest=_MANIFEST,
    artifact_integrities=(_INTEGRITY,),
)


def test_renderer_emits_canonical_build_evidence_json() -> None:
    rendered = BuildEvidenceJsonRenderer().render(_EVIDENCE)

    payload = json.loads(rendered)

    assert payload["build_id"] == str(_BUILD_ID)

    assert payload["source"] == {
        "revision": _SOURCE_STATE.revision,
        "dirty": False,
    }

    assert payload["dependency_state"] == {
        "declaration": {
            "identity": "pyproject.toml",
            "sha256": "c" * 64,
        },
        "lock": {
            "identity": "requirements.txt",
            "sha256": "d" * 64,
        },
    }

    assert payload["effective_configuration"] == {
        "profile": "ci",
        "target": "familyos-cli-package",
        "functional_validation": False,
        "evidence_required": True,
        "evidence_requested": True,
        "target_supported": True,
    }

    assert payload["validation"]["profile"] == "ci"
    assert payload["validation"]["status"] == "passed"

    assert payload["validation"]["checks"] == [
        {
            "check_id": "artifact-integrity",
            "domain": "integrity",
            "requirement": "required",
            "status": "passed",
            "diagnostic": None,
        }
    ]

    assert payload["artifact_manifest"]["build_id"] == str(_BUILD_ID)
    assert len(payload["artifact_manifest"]["entries"]) == 1

    manifest_entry = payload["artifact_manifest"]["entries"][0]

    assert manifest_entry == {
        "logical_name": "familyos-cli",
        "artifact_type": "python-wheel",
        "version": "0.1.0",
        "size": 1024,
        "path": str(_ARTIFACT_PATH),
        "digest_algorithm": "sha256",
        "digest": "b" * 64,
        "structural_validation_status": "valid",
    }

    assert payload["artifact_integrities"] == [
        {
            "logical_name": "familyos-cli",
            "artifact_type": "python-wheel",
            "version": "0.1.0",
            "size": 1024,
            "path": str(_ARTIFACT_PATH),
            "source_revision": _SOURCE_STATE.revision,
            "algorithm": "sha256",
            "digest": "b" * 64,
        }
    ]


def test_renderer_terminates_json_with_newline() -> None:
    rendered = BuildEvidenceJsonRenderer().render(_EVIDENCE)

    assert rendered.endswith("\n")


def test_dependency_state_is_portable_across_checkout_roots(
    tmp_path: Path,
) -> None:
    first_root = tmp_path / "first-checkout"
    second_root = tmp_path / "second-checkout"

    first = replace(
        _EVIDENCE,
        dependency_state=DependencyState(
            declaration_path=first_root / "pyproject.toml",
            declaration_digest="c" * 64,
            lock_path=first_root / "requirements.txt",
            lock_digest="d" * 64,
        ),
    )
    second = replace(
        _EVIDENCE,
        dependency_state=DependencyState(
            declaration_path=second_root / "pyproject.toml",
            declaration_digest="c" * 64,
            lock_path=second_root / "requirements.txt",
            lock_digest="d" * 64,
        ),
    )

    first_rendered = BuildEvidenceJsonRenderer().render(first)
    second_rendered = BuildEvidenceJsonRenderer().render(second)

    assert first_rendered == second_rendered
    assert str(first_root) not in first_rendered
    assert str(second_root) not in second_rendered


def test_effective_configuration_is_portable_across_checkout_roots(
    tmp_path: Path,
) -> None:
    first_root = tmp_path / "first-checkout"
    second_root = tmp_path / "second-checkout"

    first = replace(
        _EVIDENCE,
        effective_configuration=replace(
            _EFFECTIVE_CONFIGURATION,
            output_dir=first_root / "dist",
            evidence_output=first_root / "build-evidence.json",
        ),
    )
    second = replace(
        _EVIDENCE,
        effective_configuration=replace(
            _EFFECTIVE_CONFIGURATION,
            output_dir=second_root / "dist",
            evidence_output=second_root / "build-evidence.json",
        ),
    )

    first_rendered = BuildEvidenceJsonRenderer().render(first)
    second_rendered = BuildEvidenceJsonRenderer().render(second)

    assert first_rendered == second_rendered
    assert str(first_root) not in first_rendered
    assert str(second_root) not in second_rendered
