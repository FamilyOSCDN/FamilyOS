"""P4 raw evidence remains distinct from Quality acceptance and attribution."""

import hashlib
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from scripts import capture_quality_source as p4
from scripts import run_quality_ci as adapter


@pytest.fixture
def source(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "source with spaces"
    root.mkdir()
    (root / "tracked.txt").write_text("original", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], cwd=root, check=True)
    return root, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def capture(source: tuple[Path, str], output: Path, phase: str, **kwargs: Any) -> int:
    root, revision = source
    return p4.capture(phase=phase, repository=root, expected_revision=revision,
                      output_dir=output, run_id="123", run_attempt="1", event="pull_request", **kwargs)


def record(output: Path) -> dict[str, Any]:
    value: dict[str, Any] = json.loads((output / "p4-capture.json").read_text())
    return value


def test_exact_bytes_return_codes_and_fresh_sidecar_do_not_dirty_source(source: tuple[Path, str], tmp_path: Path) -> None:
    output = tmp_path / "p4"
    assert capture(source, output, "before") == 0
    assert record(output)["measurement"]["triggered"] is None
    assert capture(source, output, "after") == 0
    assert record(output)["measurement"] == {
        "eligible": True, "triggered": False, "reasons": [], "state": "clean", "source_modified_before": False,
    }
    for phase in ("before", "after"):
        assert (output / f"head-{phase}").read_bytes() == (source[1] + "\n").encode()
        assert (output / f"status-{phase}").read_bytes() == b""
        sample = record(output)[phase]
        for name in ("head", "status"):
            command = sample[name]
            assert command["exit_code"] == 0 and command["error"] is None
            for channel in ("stdout", "stderr"):
                data = (output / command[channel]["file"]).read_bytes()
                assert hashlib.sha256(data).hexdigest() == command[channel]["sha256"]
    assert subprocess.check_output(["git", "status", "--porcelain"], cwd=source[0]) == b""


def test_per_file_untracked_capture_and_unattributed_modification(source: tuple[Path, str], tmp_path: Path) -> None:
    output = tmp_path / "p4"
    capture(source, output, "before")
    nested = source[0] / "new folder"
    nested.mkdir()
    (nested / "a.txt").write_text("a")
    (nested / "b.txt").write_text("b")
    capture(source, output, "after")
    raw = (output / "status-after").read_text()
    assert "a.txt" in raw and "b.txt" in raw
    assert record(output)["measurement"]["triggered"] is True
    assert record(output)["attribution"] == {"status": "unattributed", "tool": None, "version": None, "cause": None, "evidence": []}
    with pytest.raises(ValueError, match="clean"):
        adapter.checked_revision(source[0], source[1])


def test_changed_head_is_a_trigger_even_when_status_is_clean(source: tuple[Path, str], tmp_path: Path) -> None:
    output = tmp_path / "p4"
    capture(source, output, "before")
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-qm", "new revision"], cwd=source[0], check=True)
    capture(source, output, "after")
    assert record(output)["after"]["state"] == "clean"
    assert record(output)["measurement"]["triggered"] is True


@pytest.mark.parametrize("phase", ["before", "after"])
def test_missing_capture_is_unavailable_not_zero(source: tuple[Path, str], tmp_path: Path, phase: str) -> None:
    output = tmp_path / "p4"
    assert capture(source, output, phase) == 0
    measurement = record(output)["measurement"]
    assert measurement["eligible"] is False and measurement["triggered"] is None
    assert measurement["state"] == "unavailable"
    assert measurement["reasons"] == ["after_missing" if phase == "before" else "before_missing"]


def test_preexisting_dirty_source_is_not_an_eligible_p4_trigger(source: tuple[Path, str], tmp_path: Path) -> None:
    output = tmp_path / "p4"
    (source[0] / "tracked.txt").write_text("already dirty")
    capture(source, output, "before")
    capture(source, output, "after")
    measurement = record(output)["measurement"]
    assert measurement["source_modified_before"] is True
    assert measurement["eligible"] is False and measurement["triggered"] is None
    assert measurement["reasons"] == ["source_modified_before"]


@pytest.mark.parametrize("problem", ["nonzero", "timeout", "missing-git"])
def test_git_failure_preserves_diagnostics_and_still_attempts_status(source: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch, problem: str) -> None:
    original = subprocess.run
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
        calls.append(command)
        if command[1] == "rev-parse":
            if problem == "timeout":
                raise subprocess.TimeoutExpired(command, 30, output=b"partial", stderr=b"timeout diagnostic")
            if problem == "missing-git":
                raise FileNotFoundError("git missing")
            return subprocess.CompletedProcess(command, 128, b"", b"fatal diagnostic\n")
        return original(command, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)
    output = tmp_path / "p4"
    assert capture(source, output, "before") == 0
    assert calls[-1] == ["git", "status", "--porcelain=v1", "--untracked-files=all"]
    assert record(output)["before"]["state"] == "unavailable"
    assert record(output)["measurement"]["triggered"] is None
    if problem == "nonzero":
        assert (output / "head-before.stderr").read_bytes() == b"fatal diagnostic\n"
        assert record(output)["before"]["head"]["exit_code"] == 128
    if problem == "timeout":
        assert (output / "head-before").read_bytes() == b"partial"


def test_separate_after_capture_survives_adapter_crash_before_its_postflight(source: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original = subprocess.run
    cli_calls: list[list[str]] = []

    def run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[Any]:
        if command[0] == "familyos":
            cli_calls.append(command)
            (source[0] / "tracked.txt").write_text("changed before crash")
            raise OSError("early CLI crash")
        return original(command, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)
    output, quality_output = tmp_path / "p4", tmp_path / "quality"
    capture(source, output, "before")
    assert adapter.run(repository=source[0], expected_revision=source[1], output_dir=quality_output) == 2
    assert capture(source, output, "after", quality_output=quality_output, quality_step_outcome="failure") == 0
    assert len(cli_calls) == 1
    assert record(output)["measurement"]["triggered"] is True
    assert record(output)["correlation"]["available"] is False
    execution = json.loads((quality_output / "execution.json").read_text())
    assert execution["report_accepted"] is False and "early CLI crash" in execution["adapter_error"]


def test_duration_correlation_has_no_invented_executor_windows(source: tuple[Path, str], tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]]) -> None:
    output, quality_output = tmp_path / "p4", tmp_path / "quality"
    quality_output.mkdir()
    report = ci_report_factory(*source)
    report["check_results"][0]["duration_seconds"] = 1.25
    report["check_results"][0]["evidence"][0].update(tool="ruff", tool_version="ruff fixture")
    (quality_output / "quality-report.json").write_text(json.dumps(report))
    (quality_output / "execution.json").write_text(json.dumps({"revision": source[1], "report_accepted": False}))
    capture(source, output, "before")
    capture(source, output, "after", quality_output=quality_output)
    correlation = record(output)["correlation"]
    assert correlation["available"] is True and correlation["report_accepted"] is False
    assert correlation["checks"][0] == {"check_id": "QLT-CHECK-RUFF", "duration_seconds": 1.25, "tools": [{"tool": "ruff", "version": "ruff fixture"}]}
    assert "no executor start timestamps" in correlation["timing_semantics"]
    assert record(output)["attribution"]["tool"] is None


def test_capture_refuses_existing_or_overlapping_evidence(source: tuple[Path, str], tmp_path: Path) -> None:
    output = tmp_path / "p4"
    capture(source, output, "before")
    preserved = {p.name: p.read_bytes() for p in output.iterdir()}
    assert capture(source, output, "before") == 2
    assert {p.name: p.read_bytes() for p in output.iterdir()} == preserved
    assert capture(source, source[0] / "p4", "before") == 2
    assert capture(source, tmp_path / "nested" / "p4", "before", quality_output=tmp_path / "nested") == 2


def test_logs_escape_file_names_and_do_not_capture_unrelated_environment(source: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("UNRELATED_SECRET", "do-not-capture-this")
    (source[0] / "::error::untrusted\nname").write_text("content must not be collected")
    output = tmp_path / "p4"
    capture(source, output, "before")
    logs = capsys.readouterr().out
    assert all(line.startswith("{") for line in logs.splitlines())
    retained = "".join(p.read_text(errors="replace") for p in output.iterdir())
    assert "do-not-capture-this" not in retained
    assert "content must not be collected" not in retained
