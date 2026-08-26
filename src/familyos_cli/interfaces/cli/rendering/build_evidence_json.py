"""Deterministic JSON renderer for canonical Build Evidence."""

from __future__ import annotations

import json
from typing import Any

from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifestEntry,
)
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
)


class BuildEvidenceJsonRenderer:
    """Project canonical Build Evidence into stable machine-readable JSON."""

    def render(self, evidence: BuildEvidence) -> str:
        """Render Build Evidence as UTF-8-compatible deterministic JSON."""

        payload: dict[str, Any] = {
            "build_id": str(evidence.build_id),
            "build_context_fingerprint": {
                "algorithm": evidence.build_context_fingerprint.algorithm,
                "digest": evidence.build_context_fingerprint.digest,
            },
            "source": {
                "revision": evidence.source_state.revision,
                "dirty": evidence.source_state.dirty,
            },
            "runtime": {
                "version": evidence.runtime_version,
            },
            "dependency_state": {
                "declaration": {
                    "identity": evidence.dependency_state.declaration_path.name,
                    "sha256": evidence.dependency_state.declaration_digest,
                },
                "lock": {
                    "identity": evidence.dependency_state.lock_path.name,
                    "sha256": evidence.dependency_state.lock_digest,
                },
            },
            "toolchain": {
                "critical_versions": [
                    {
                        "distribution": version.distribution,
                        "version": version.version,
                    }
                    for version in evidence.toolchain_state.critical_versions
                ],
            },
            "environment": {
                "operating_system": (
                    evidence.environment_state.operating_system
                ),
                "operating_system_release": (
                    evidence.environment_state.operating_system_release
                ),
                "machine_architecture": (
                    evidence.environment_state.machine_architecture
                ),
                "virtual_environment_active": (
                    evidence.environment_state.virtual_environment_active
                ),
                "temporary_directory": (
                    evidence.environment_state.temporary_directory
                ),
                "filesystem_encoding": (
                    evidence.environment_state.filesystem_encoding
                ),
            },
            "effective_configuration": {
                "profile": evidence.effective_configuration.profile.value,
                "target": evidence.effective_configuration.target.value,
                "functional_validation": (
                    evidence.effective_configuration.functional_validation
                ),
                "evidence_required": (
                    evidence.effective_configuration.evidence_required
                ),
                "evidence_requested": (
                    evidence.effective_configuration.evidence_requested
                ),
                "target_supported": (
                    evidence.effective_configuration.target_supported
                ),
            },
            "execution": {
                "stages": [
                    {
                        "stage": observation.stage.value,
                        "status": observation.status.value,
                        "duration_seconds": observation.duration_seconds,
                        "diagnostic": observation.diagnostic,
                    }
                    for observation in evidence.execution_observations
                ],
            },
            "validation": {
                "profile": evidence.validation_result.profile.value,
                "status": evidence.validation_result.status.value,
                "checks": [
                    self._validation_check_payload(check)
                    for check in evidence.validation_result.checks
                ],
            },
            "artifact_manifest": {
                "build_id": str(evidence.artifact_manifest.build_id),
                "entries": [
                    self._manifest_entry_payload(entry)
                    for entry in evidence.artifact_manifest.entries
                ],
            },
            "artifact_integrities": [
                self._artifact_integrity_payload(integrity)
                for integrity in evidence.artifact_integrities
            ],
        }

        return f"{json.dumps(payload, indent=2, ensure_ascii=True)}\n"

    @staticmethod
    def _validation_check_payload(
        check: BuildValidationCheckResult,
    ) -> dict[str, Any]:
        return {
            "check_id": check.check_id,
            "domain": check.domain.value,
            "requirement": check.requirement.value,
            "status": check.status.value,
            "diagnostic": check.diagnostic,
        }

    @staticmethod
    def _manifest_entry_payload(
        entry: ArtifactManifestEntry,
    ) -> dict[str, Any]:
        return {
            "logical_name": entry.logical_name,
            "artifact_type": entry.artifact_type.value,
            "version": entry.version,
            "size": entry.size,
            "path": str(entry.path),
            "digest_algorithm": entry.digest_algorithm.value,
            "digest": entry.digest,
            "structural_validation_status": (
                entry.structural_validation_status.value
            ),
        }

    @staticmethod
    def _artifact_integrity_payload(
        integrity: ArtifactIntegrity,
    ) -> dict[str, Any]:
        identity = integrity.artifact_identity

        return {
            "logical_name": identity.logical_name,
            "artifact_type": identity.artifact_type.value,
            "version": identity.version,
            "size": identity.size,
            "path": str(identity.path),
            "source_revision": identity.source_revision,
            "algorithm": integrity.algorithm.value,
            "digest": integrity.digest,
        }
