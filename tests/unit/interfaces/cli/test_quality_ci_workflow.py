"""Workflow boundaries for the initial Quality observation integration."""

from pathlib import Path
from typing import Any

import yaml


def job() -> dict[str, Any]:
    workflow = yaml.safe_load(Path(".github/workflows/ci.yml").read_text())
    result: dict[str, Any] = workflow["jobs"]["quality-observation"]
    return result


def test_quality_observation_is_independent_and_nonblocking() -> None:
    quality = job()
    assert quality["continue-on-error"] is True
    assert quality["timeout-minutes"] == 30
    assert "needs" not in quality
    workflow = yaml.safe_load(Path(".github/workflows/ci.yml").read_text())
    for name, other in workflow["jobs"].items():
        if name != "quality-observation":
            assert "quality-observation" not in str(other.get("needs", ""))


def test_quality_job_uses_existing_runtime_and_locked_installation() -> None:
    steps = job()["steps"]
    setup = next(step for step in steps if step.get("uses", "").startswith("actions/setup-python@"))
    assert setup["with"]["python-version"] == "3.13"
    assert setup["with"]["cache-dependency-path"] == "requirements.txt"
    commands = [step.get("run", "") for step in steps]
    assert "python -m pip install -r requirements.txt" in commands
    assert "python -m pip install --no-deps --no-build-isolation -e ." in commands


def test_quality_job_binds_to_actual_event_revision_and_preserves_artifacts() -> None:
    steps = job()["steps"]
    execute = next(step for step in steps if step.get("id") == "quality_observation")
    assert "continue-on-error" not in execute
    command = execute["run"]
    assert "python -m scripts.run_quality_ci" in command
    for argument in (
        '--repository "$GITHUB_WORKSPACE"', '--expected-revision "$GITHUB_SHA"',
        '--output-dir "$RUNNER_TEMP/familyos-quality-$GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT"',
        '--summary "$GITHUB_STEP_SUMMARY"',
    ):
        assert argument in command
    assert "${{" not in command
    upload = next(step for step in steps if step.get("uses", "").startswith("actions/upload-artifact@"))
    assert upload["if"] == "always()"
    assert upload["with"]["name"] == "familyos-quality-observation"
    assert upload["with"]["if-no-files-found"] == "error"
    assert upload["with"]["path"] == "${{ runner.temp }}/familyos-quality-${{ github.run_id }}-${{ github.run_attempt }}/"
