"""Canonical structured-report fixtures for CI transport tests."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from familyos_cli.application.quality import REPOSITORY_PROFILE


@pytest.fixture
def ci_report_factory() -> Callable[[Path, str], dict[str, Any]]:
    def make(repository: Path, revision: str) -> dict[str, Any]:
        target: dict[str, Any] = {
            "target_type": "repository", "identifier": "familyos-cli", "revision": revision,
            "version": None, "path": str(repository.resolve()), "metadata": [],
        }
        checks: list[dict[str, Any]] = []
        for check_id in REPOSITORY_PROFILE.required_checks:
            evidence_id = str(check_id).replace("QLT-CHECK-", "QLT-EVID-")
            evidence: dict[str, Any] = {
                "id": evidence_id, "type": "TEST", "source": "test", "target": target,
                "result": "PASS", "created_at": "2026-09-03T12:00:00+00:00",
                "revision": revision, "rule_id": None, "requirement_id": None,
                "tool": None, "tool_version": None, "metadata": [], "artifact": None,
            }
            checks.append({
                "check_id": str(check_id), "status": "PASS", "findings": [],
                "evidence": [evidence], "duration_seconds": 0.1, "diagnostics": [],
            })
        return {
            "schema_version": "1.0.0",
            "assessment": {
                "id": "QLT-ASMT-TEST", "target": target, "revision": revision,
                "profile": REPOSITORY_PROFILE.reference, "status": "PASS", "quality_state": "PASS",
                "evidence_ids": sorted(check["evidence"][0]["id"] for check in checks),
                "finding_ids": [], "created_at": "2026-09-03T12:00:00+00:00",
            },
            "check_results": checks,
        }
    return make
