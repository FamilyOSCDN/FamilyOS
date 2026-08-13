"""Tests for subprocess-backed validation gates."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.subprocess_gate import (
    SubprocessValidationGate,
)


def _gate(tmp_path: Path) -> SubprocessValidationGate:
    return SubprocessValidationGate(
        gate_id="ruff",
        command=("python", "-m", "ruff"),
        cwd=tmp_path,
    )


def test_subprocess_exit_zero_passes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "ok", ""),
    )

    result = _gate(tmp_path).execute()

    assert result.status is ValidationStatus.PASSED
    assert result.exit_code == 0


def test_subprocess_nonzero_fails_with_normalized_diagnostic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    message = f"{tmp_path}/src/module.py: validation failed"
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 2, "", message),
    )

    result = _gate(tmp_path).execute()

    assert result.status is ValidationStatus.FAILED
    assert result.exit_code == 2
    assert result.diagnostic == "./src/module.py: validation failed"
    assert str(tmp_path) not in result.diagnostic


def test_subprocess_launch_failure_is_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise OSError(f"cannot launch from {tmp_path}")

    monkeypatch.setattr(subprocess, "run", fail)

    result = _gate(tmp_path).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.exit_code is None
    assert result.diagnostic == "cannot launch from ."
