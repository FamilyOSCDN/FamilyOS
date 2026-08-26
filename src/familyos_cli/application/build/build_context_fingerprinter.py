"""Deterministically fingerprint canonical Build Context inputs."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from familyos_cli.application.build.build_context import BuildContext
from familyos_cli.application.build.build_context_fingerprint import (
    BuildContextFingerprint,
)


class BuildContextFingerprinter:
    """Project Build Context into canonical semantic inputs and fingerprint it."""

    def fingerprint(
        self,
        context: BuildContext,
    ) -> BuildContextFingerprint:
        """Return the SHA-256 fingerprint of canonical Build Context inputs."""

        payload = self.canonical_payload(context)
        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")

        return BuildContextFingerprint(
            algorithm="sha256",
            digest=hashlib.sha256(encoded).hexdigest(),
        )

    def canonical_payload(
        self,
        context: BuildContext,
    ) -> dict[str, Any]:
        """Return the canonical semantic projection of Build Context."""

        revision = context.source_state.revision
        if revision is None or not revision:
            raise ValueError(
                "Build Context fingerprint requires a captured source revision"
            )

        return {
            "schema": "familyos.build-context-fingerprint.v1",
            "source": {
                "revision": revision,
                "dirty": context.source_state.dirty,
            },
            "runtime": {
                "version": context.runtime_version,
            },
            "dependencies": {
                "declaration": {
                    "identity": context.dependency_state.declaration_path.name,
                    "sha256": context.dependency_state.declaration_digest,
                },
                "lock": {
                    "identity": context.dependency_state.lock_path.name,
                    "sha256": context.dependency_state.lock_digest,
                },
            },
            "toolchain": {
                "critical_versions": [
                    {
                        "distribution": component.distribution,
                        "version": component.version,
                    }
                    for component in sorted(
                        context.toolchain_state.critical_versions,
                        key=lambda component: component.distribution,
                    )
                ],
            },
            "environment": {
                "operating_system": (
                    context.environment_state.operating_system
                ),
                "operating_system_release": (
                    context.environment_state.operating_system_release
                ),
                "machine_architecture": (
                    context.environment_state.machine_architecture
                ),
                "filesystem_encoding": (
                    context.environment_state.filesystem_encoding
                ),
            },
            "configuration": {
                "profile": context.profile.value,
                "target": context.target.value,
                "functional_validation": (
                    context.effective_configuration.functional_validation
                ),
            },
        }
