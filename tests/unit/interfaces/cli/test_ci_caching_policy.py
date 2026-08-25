"""Structural caching contract for canonical CI automation."""

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


def _validate_job() -> dict[object, object]:
    workflow = _workflow()

    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict)

    validate = jobs.get("validate")
    assert isinstance(validate, dict)

    return validate


def _steps() -> list[dict[object, object]]:
    steps = _validate_job().get("steps")
    assert isinstance(steps, list)

    normalized: list[dict[object, object]] = []

    for step in steps:
        assert isinstance(step, dict)
        normalized.append(step)

    return normalized


def _step_named(name: str) -> dict[object, object]:
    matches = [
        step
        for step in _steps()
        if step.get("name") == name
    ]

    assert len(matches) == 1, matches
    return matches[0]


def test_python_setup_enables_only_pip_dependency_cache() -> None:
    step = _step_named("Set up Python 3.13")

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("cache") == "pip"


def test_pip_cache_identity_uses_canonical_dependency_state() -> None:
    step = _step_named("Set up Python 3.13")

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert (
        configuration.get("cache-dependency-path")
        == "requirements.txt"
    )


def test_pip_cache_identity_retains_explicit_runtime_state() -> None:
    step = _step_named("Set up Python 3.13")

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("python-version") == "3.13"


def test_dependency_install_remains_authoritative_on_cache_miss() -> None:
    step = _step_named("Install locked dependencies")

    assert (
        step.get("run")
        == "python -m pip install -r requirements.txt"
    )


def test_familyos_install_does_not_depend_on_cached_environment() -> None:
    step = _step_named(
        "Install FamilyOS without dependency resolution"
    )

    assert (
        step.get("run")
        == (
            "python -m pip install "
            "--no-deps --no-build-isolation -e ."
        )
    )


def test_ci_does_not_cache_authoritative_build_outputs() -> None:
    forbidden_paths = (
        ".venv",
        "dist",
        "build",
        "build-evidence.json",
        "ci-validation.json",
    )

    for step in _steps():
        uses = step.get("uses")

        if not isinstance(uses, str):
            continue

        is_cache_action = (
            uses.startswith("actions/cache@")
            or uses.startswith("actions/setup-python@")
        )

        if not is_cache_action:
            continue

        configuration = step.get("with")
        assert isinstance(configuration, dict)

        serialized = "\\n".join(
            f"{key}={value}"
            for key, value in configuration.items()
        )

        for forbidden in forbidden_paths:
            assert forbidden not in serialized


def _cache_free_job() -> dict[object, object]:
    workflow = _workflow()

    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict)

    job = jobs.get("cache-free-validation")
    assert isinstance(job, dict)

    return job


def _cache_free_steps() -> list[dict[object, object]]:
    steps = _cache_free_job().get("steps")
    assert isinstance(steps, list)

    normalized: list[dict[object, object]] = []

    for step in steps:
        assert isinstance(step, dict)
        normalized.append(step)

    return normalized


def _cache_free_step_named(
    name: str,
) -> dict[object, object]:
    matches = [
        step
        for step in _cache_free_steps()
        if step.get("name") == name
    ]

    assert len(matches) == 1, matches
    return matches[0]


def test_ci_schedules_periodic_cache_free_validation() -> None:
    workflow = _workflow()

    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict)

    schedule = triggers.get("schedule")
    assert isinstance(schedule, list)
    assert schedule


def test_cache_free_job_runs_only_for_explicit_recovery_events() -> None:
    job = _cache_free_job()

    assert job.get("if") == (
        "github.event_name == 'schedule' || "
        "github.event_name == 'workflow_dispatch'"
    )


def test_cache_free_python_setup_does_not_restore_dependency_cache() -> None:
    step = _cache_free_step_named(
        "Set up Python 3.13 without cache"
    )

    configuration = step.get("with")
    assert isinstance(configuration, dict)

    assert configuration.get("python-version") == "3.13"
    assert "cache" not in configuration
    assert "cache-dependency-path" not in configuration


def test_cache_free_dependency_install_disables_pip_cache() -> None:
    step = _cache_free_step_named(
        "Install locked dependencies without cache"
    )

    assert (
        step.get("run")
        == (
            "python -m pip install "
            "--no-cache-dir -r requirements.txt"
        )
    )


def test_cache_free_familyos_install_remains_canonical() -> None:
    step = _cache_free_step_named(
        "Install FamilyOS without dependency resolution"
    )

    assert (
        step.get("run")
        == (
            "python -m pip install "
            "--no-deps --no-build-isolation -e ."
        )
    )


def test_cache_free_job_runs_canonical_validation_and_build() -> None:
    steps = _cache_free_steps()

    commands: set[str] = set()

    for step in steps:
        command = step.get("run")

        if isinstance(command, str):
            commands.add(command)

    assert (
        "familyos validation ci --output ci-validation.json"
        in commands
    )

    assert any(
        "familyos build" in command
        and "--profile ci" in command
        and "--output-dir dist" in command
        and "--evidence-output build-evidence.json" in command
        for command in commands
    )


def test_ci_exposes_manual_cache_free_recovery_trigger() -> None:
    workflow = _workflow()

    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict)

    assert "workflow_dispatch" in triggers


def test_cache_free_job_supports_periodic_and_manual_recovery() -> None:
    job = _cache_free_job()

    assert job.get("if") == (
        "github.event_name == 'schedule' || "
        "github.event_name == 'workflow_dispatch'"
    )


def test_manual_cache_recovery_remains_non_authoritative() -> None:
    step = _cache_free_step_named(
        "Install locked dependencies without cache"
    )

    command = step.get("run")
    assert isinstance(command, str)

    assert "--no-cache-dir" in command
    assert "-r requirements.txt" in command
    assert "pip cache" not in command
