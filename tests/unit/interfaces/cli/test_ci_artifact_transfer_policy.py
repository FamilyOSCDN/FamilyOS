"""Structural contract for canonical CI artifact transfer."""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW_PATH = Path(".github/workflows/ci.yml")


def _workflow() -> dict[object, object]:
    loaded = yaml.safe_load(
        WORKFLOW_PATH.read_text(encoding="utf-8")
    )
    assert isinstance(loaded, dict)
    return loaded


def _jobs() -> dict[object, object]:
    jobs = _workflow().get("jobs")
    assert isinstance(jobs, dict)
    return jobs


def _job_named(name: str) -> dict[object, object]:
    job = _jobs().get(name)
    assert isinstance(job, dict)
    return job


def _steps(job: dict[object, object]) -> list[dict[object, object]]:
    raw_steps = job.get("steps")
    assert isinstance(raw_steps, list)

    steps: list[dict[object, object]] = []

    for raw_step in raw_steps:
        assert isinstance(raw_step, dict)
        steps.append(raw_step)

    return steps


def test_ci_has_distinct_artifact_consumer_job() -> None:
    jobs = _jobs()

    assert "artifact-validation" in jobs


def test_artifact_consumer_depends_on_canonical_build_job() -> None:
    job = _job_named("artifact-validation")

    needs = job.get("needs")

    assert needs == "validate"


def test_artifact_consumer_does_not_rebuild_package() -> None:
    job = _job_named("artifact-validation")

    commands = [
        step.get("run")
        for step in _steps(job)
        if isinstance(step.get("run"), str)
    ]

    forbidden_markers = (
        "familyos build",
        "python -m build",
    )

    for command in commands:
        assert isinstance(command, str)

        for marker in forbidden_markers:
            assert marker not in command


def _step_named(
    job_name: str,
    step_name: str,
) -> dict[object, object]:
    job = _job_named(job_name)

    matches = [
        step
        for step in _steps(job)
        if step.get("name") == step_name
    ]

    assert len(matches) == 1, matches
    return matches[0]


def test_build_job_uploads_canonical_package_candidates() -> None:
    step = _step_named(
        "validate",
        "Upload package candidates",
    )

    uses = step.get("uses")
    assert isinstance(uses, str)
    assert uses.startswith("actions/upload-artifact@")

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("name") == (
        "familyos-package-candidates"
    )
    assert configuration.get("path") == "dist/"


def test_artifact_consumer_downloads_same_package_candidates() -> None:
    step = _step_named(
        "artifact-validation",
        "Download package candidates",
    )

    uses = step.get("uses")
    assert isinstance(uses, str)

    assert uses.startswith(
        "actions/download-artifact@"
    )

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("name") == (
        "familyos-package-candidates"
    )
    assert configuration.get("path") == "dist"


def test_download_artifact_action_is_pinned_to_commit_sha() -> None:
    step = _step_named(
        "artifact-validation",
        "Download package candidates",
    )

    uses = step.get("uses")
    assert isinstance(uses, str)

    import re

    assert re.fullmatch(
        r"actions/download-artifact@[0-9a-fA-F]{40}",
        uses,
    )


def test_build_job_uploads_canonical_build_evidence() -> None:
    step = _step_named(
        "validate",
        "Upload canonical Build Evidence",
    )

    uses = step.get("uses")
    assert isinstance(uses, str)
    assert uses.startswith("actions/upload-artifact@")

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("name") == "familyos-build-evidence"
    assert configuration.get("path") == "build-evidence.json"


def test_artifact_consumer_downloads_canonical_build_evidence() -> None:
    step = _step_named(
        "artifact-validation",
        "Download canonical Build Evidence",
    )

    uses = step.get("uses")
    assert isinstance(uses, str)

    assert uses.startswith(
        "actions/download-artifact@"
    )

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("name") == "familyos-build-evidence"
    assert configuration.get("path") == "evidence"


def test_downloaded_evidence_remains_separate_from_candidate_bytes() -> None:
    candidate_step = _step_named(
        "artifact-validation",
        "Download package candidates",
    )
    evidence_step = _step_named(
        "artifact-validation",
        "Download canonical Build Evidence",
    )

    candidate_configuration = candidate_step.get("with")
    evidence_configuration = evidence_step.get("with")

    assert isinstance(candidate_configuration, dict)
    assert isinstance(evidence_configuration, dict)

    assert candidate_configuration.get("path") == "dist"
    assert evidence_configuration.get("path") == "evidence"


def test_artifact_consumer_verifies_downloaded_integrity() -> None:
    step = _step_named(
        "artifact-validation",
        "Verify transferred artifact integrity",
    )

    command = step.get("run")
    assert isinstance(command, str)

    assert "evidence/build-evidence.json" in command
    assert "artifact_integrities" in command
    assert "hashlib.sha256" in command


def test_integrity_verification_rejects_missing_or_changed_artifacts() -> None:
    step = _step_named(
        "artifact-validation",
        "Verify transferred artifact integrity",
    )

    command = step.get("run")
    assert isinstance(command, str)

    required_markers = (
        "missing",
        "digest mismatch",
        "unexpected",
        "raise SystemExit",
    )

    for marker in required_markers:
        assert marker in command


def test_integrity_verification_uses_downloaded_candidates_only() -> None:
    step = _step_named(
        "artifact-validation",
        "Verify transferred artifact integrity",
    )

    command = step.get("run")
    assert isinstance(command, str)

    assert 'Path("dist")' in command
    assert 'Path("evidence/build-evidence.json")' in command

    assert "familyos build" not in command
    assert "python -m build" not in command


def _integrity_verification_command() -> str:
    step = _step_named(
        "artifact-validation",
        "Verify transferred artifact integrity",
    )

    command = step.get("run")
    assert isinstance(command, str)

    return command


def _python_body_from_verification_command() -> str:
    command = _integrity_verification_command()

    marker = "python - <<'PY'\n"
    assert command.startswith(marker)
    assert command.endswith("\nPY\n")

    return command[
        len(marker) : -len("\nPY\n")
    ]


def _execute_verification(
    tmp_path: Path,
    *,
    artifact_bytes: bytes,
    expected_digest: str,
    mutate_after_evidence: bool = False,
    omit_artifact: bool = False,
    unexpected_artifact: bool = False,
) -> None:
    import json

    dist = tmp_path / "dist"
    evidence = tmp_path / "evidence"

    dist.mkdir()
    evidence.mkdir()

    artifact = dist / "familyos_test.whl"

    if not omit_artifact:
        artifact.write_bytes(artifact_bytes)

    payload = {
        "artifact_integrities": [
            {
                "path": "dist/familyos_test.whl",
                "algorithm": "sha256",
                "digest": expected_digest,
            }
        ]
    }

    (evidence / "build-evidence.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    if mutate_after_evidence and artifact.exists():
        artifact.write_bytes(artifact_bytes + b"x")

    if unexpected_artifact:
        (dist / "unexpected.whl").write_bytes(b"unexpected")

    body = _python_body_from_verification_command()

    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-c", body],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    if (
        mutate_after_evidence
        or omit_artifact
        or unexpected_artifact
    ):
        assert result.returncode != 0
    else:
        assert result.returncode == 0, (
            result.stdout,
            result.stderr,
        )


def test_transferred_integrity_verification_accepts_identical_bytes(
    tmp_path: Path,
) -> None:
    import hashlib

    payload = b"canonical-artifact"

    _execute_verification(
        tmp_path,
        artifact_bytes=payload,
        expected_digest=hashlib.sha256(payload).hexdigest(),
    )


def test_transferred_integrity_verification_rejects_mutated_bytes(
    tmp_path: Path,
) -> None:
    import hashlib

    payload = b"canonical-artifact"

    _execute_verification(
        tmp_path,
        artifact_bytes=payload,
        expected_digest=hashlib.sha256(payload).hexdigest(),
        mutate_after_evidence=True,
    )


def test_transferred_integrity_verification_rejects_missing_artifact(
    tmp_path: Path,
) -> None:
    import hashlib

    payload = b"canonical-artifact"

    _execute_verification(
        tmp_path,
        artifact_bytes=payload,
        expected_digest=hashlib.sha256(payload).hexdigest(),
        omit_artifact=True,
    )


def test_transferred_integrity_verification_rejects_unexpected_artifact(
    tmp_path: Path,
) -> None:
    import hashlib

    payload = b"canonical-artifact"

    _execute_verification(
        tmp_path,
        artifact_bytes=payload,
        expected_digest=hashlib.sha256(payload).hexdigest(),
        unexpected_artifact=True,
    )
