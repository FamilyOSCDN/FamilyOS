"""Construct Build Provenance from established Build Evidence."""

from __future__ import annotations

from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_provenance import BuildProvenance


class BuildProvenanceFactory:
    """Project canonical provenance from existing Build Evidence."""

    def from_build_evidence(
        self,
        evidence: BuildEvidence,
    ) -> BuildProvenance:
        """Derive provenance without recapturing canonical build state."""

        return BuildProvenance(
            build_id=evidence.build_id,
            build_context_fingerprint=evidence.build_context_fingerprint,
            source_state=evidence.source_state,
            dependency_state=evidence.dependency_state,
            toolchain_state=evidence.toolchain_state,
            environment_state=evidence.environment_state,
            artifact_integrities=evidence.artifact_integrities,
        )
