"""CI transport invokes the public CLI once and preserves failure evidence."""

import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from scripts import run_quality_ci as adapter


@pytest.fixture
def repository(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repository with spaces"
    root.mkdir()
    (root / "source.txt").write_text("source", encoding="utf-8")
    subprocess.run(["git", "init", "--quiet"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "add", "source.txt"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Quality Test", "-c", "user.email=quality@example.invalid", "commit", "-qm", "fixture"],
        cwd=root, check=True, capture_output=True,
    )
    return root, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def install_cli(
    monkeypatch: pytest.MonkeyPatch, payload: dict[str, Any] | None,
    *, exit_code: int = 0, error: Exception | None = None,
    after: Callable[[], None] | None = None,
) -> list[list[str]]:
    original = subprocess.run
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[Any]:
        if command[0] != "familyos":
            return original(command, **kwargs)
        calls.append(command)
        if error is not None:
            raise error
        kwargs["stdout"].write(b"stdout preserved\n")
        kwargs["stderr"].write(b"stderr preserved\n")
        if payload is not None:
            Path(command[-1]).write_text(json.dumps(payload), encoding="utf-8")
        if after is not None:
            after()
        return subprocess.CompletedProcess(command, exit_code)

    monkeypatch.setattr(subprocess, "run", run)
    return calls


@pytest.mark.parametrize("exit_code", (0, 1, 2))
def test_single_canonical_invocation_preserves_exit_artifacts_and_summary(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ci_report_factory: Callable[[Path, str], dict[str, Any]], exit_code: int,
) -> None:
    root, revision = repository
    payload = ci_report_factory(root, revision)
    if exit_code == 1:
        payload["assessment"].update(status="FAIL", quality_state="FAIL")
    elif exit_code == 2:
        payload["assessment"].update(status="UNKNOWN", quality_state="UNKNOWN")
        payload["check_results"][0]["status"] = "FAIL"
    calls = install_cli(monkeypatch, payload, exit_code=exit_code)
    output = tmp_path / "artifacts"
    summary = tmp_path / "summary.md"
    summary.write_text("Existing step summary\n", encoding="utf-8")

    actual = adapter.run(repository=root, expected_revision=revision, output_dir=output, summary_path=summary)

    assert actual == exit_code
    assert calls == [[
        "familyos", "quality", "report", "--target-type", "repository", "--identifier", "familyos-cli",
        "--path", str(root), "--revision", revision, "--format", "json", "--output", str(output / "quality-report.json"),
    ]]
    gate = json.loads((output / "gate-observation.json").read_text())["gate"]
    assert gate["mode"] == "OBSERVE"
    assert gate["prevents_progression"] is False
    assert gate["decision"] == ("PASS" if exit_code == 0 else "FAIL")
    assert gate["revision"] == revision
    assert gate["assessment_id"] == payload["assessment"]["id"]
    record = json.loads((output / "execution.json").read_text())
    assert record == {
        "schema_version": "1.0.0", "revision": revision, "command": calls[0],
        "cli_exit_code": exit_code, "adapter_exit_code": exit_code, "report_accepted": True, "adapter_error": None,
    }
    assert (output / "stdout.log").read_bytes() == b"stdout preserved\n"
    assert (output / "stderr.log").read_bytes() == b"stderr preserved\n"
    assert summary.read_text() == "Existing step summary\n" + (output / "quality-summary.md").read_text()
    if exit_code == 2:
        assert "UNKNOWN / UNKNOWN" in summary.read_text()
        assert "QLT-CHECK-RUFF: FAIL" in summary.read_text()


@pytest.mark.parametrize("problem", ("wrong-revision", "tracked-change", "untracked-file"))
def test_stale_or_dirty_source_is_rejected_before_cli_execution(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch, problem: str,
) -> None:
    root, revision = repository
    if problem == "tracked-change":
        (root / "source.txt").write_text("changed", encoding="utf-8")
    elif problem == "untracked-file":
        (root / "new.py").write_text("unexpected", encoding="utf-8")
    else:
        revision = "wrong"
    calls = install_cli(monkeypatch, None)
    output = tmp_path / "artifacts"

    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    assert calls == []
    record = json.loads((output / "execution.json").read_text())
    assert record["cli_exit_code"] is None and record["report_accepted"] is False
    assert record["adapter_error"]
    assert not (output / "quality-report.json").exists()


def test_source_change_during_execution_rejects_the_report(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    root, revision = repository

    def change_source() -> None:
        (root / "source.txt").write_text("changed", encoding="utf-8")

    calls = install_cli(
        monkeypatch, ci_report_factory(root, revision),
        after=change_source,
    )
    output = tmp_path / "artifacts"
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    assert len(calls) == 1
    assert (output / "quality-report.json").exists()
    record = json.loads((output / "execution.json").read_text())
    assert record["report_accepted"] is False
    assert "clean" in record["adapter_error"]


@pytest.mark.parametrize("problem", ("missing-report", "invalid-schema", "native-error", "missing-executable"))
def test_automation_failures_remain_explicit_and_retain_logs(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ci_report_factory: Callable[[Path, str], dict[str, Any]], problem: str,
) -> None:
    root, revision = repository
    payload = ci_report_factory(root, revision)
    if problem == "invalid-schema":
        payload["schema_version"] = "future"
    calls = install_cli(
        monkeypatch, None if problem == "missing-report" else payload,
        exit_code=7 if problem == "native-error" else 0,
        error=FileNotFoundError("familyos missing") if problem == "missing-executable" else None,
    )
    output = tmp_path / "artifacts"

    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    assert len(calls) == 1
    record = json.loads((output / "execution.json").read_text())
    assert record["adapter_exit_code"] == 2
    assert not record["report_accepted"] and record["adapter_error"]
    assert (output / "stdout.log").is_file() and (output / "stderr.log").is_file()
    assert "Adapter error:" in (output / "quality-summary.md").read_text()
    if problem == "native-error":
        assert record["cli_exit_code"] == 7


def test_existing_artifact_directory_is_never_reused(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, revision = repository
    output = tmp_path / "artifacts"
    output.mkdir()
    previous = output / "quality-report.json"
    previous.write_text("previous run", encoding="utf-8")
    calls = install_cli(monkeypatch, None)
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    assert calls == []
    assert previous.read_text() == "previous run"
    assert list(output.iterdir()) == [previous]


@pytest.mark.parametrize("conflict", ("artifact-in-source", "summary-in-source", "summary-in-artifacts"))
def test_output_paths_cannot_modify_source_or_report_evidence(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch, conflict: str,
) -> None:
    root, revision = repository
    output = root / "artifacts" if conflict == "artifact-in-source" else tmp_path / "artifacts"
    summary = root / "source.txt" if conflict == "summary-in-source" else output / "execution.json"
    calls = install_cli(monkeypatch, None)
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output, summary_path=summary) == 2
    assert calls == []
    assert (root / "source.txt").read_text() == "source"
    assert not output.exists()


def test_summary_failure_preserves_report_and_marks_operational_error(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    root, revision = repository
    install_cli(monkeypatch, ci_report_factory(root, revision))
    output = tmp_path / "artifacts"
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output, summary_path=tmp_path / "absent" / "summary.md") == 2
    record = json.loads((output / "execution.json").read_text())
    assert record["report_accepted"] and record["cli_exit_code"] == 0
    assert record["adapter_exit_code"] == 2
    assert "Summary output failed" in record["adapter_error"]
    assert (output / "quality-report.json").is_file()


def test_gate_artifact_failure_is_an_explicit_automation_error(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    root, revision = repository
    payload = ci_report_factory(root, revision)
    calls = install_cli(monkeypatch, payload)
    original = Path.write_text
    def write(path: Path, data: str, *args: Any, **kwargs: Any) -> int:
        if path.name == "gate-observation.json":
            raise OSError("gate output unavailable")
        return original(path, data, *args, **kwargs)
    monkeypatch.setattr(Path, "write_text", write)
    output = tmp_path / "gate-output-failure"
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    assert len(calls) == 1
    record = json.loads((output / "execution.json").read_text())
    assert record["cli_exit_code"] == 0
    assert record["report_accepted"] is True
    assert "Gate observation output failed" in record["adapter_error"]
    assert (output / "quality-report.json").is_file()


def test_unavailable_report_produces_observation_error_without_retry(
    repository: tuple[Path, str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, revision = repository
    calls = install_cli(monkeypatch, None, exit_code=2)
    output = tmp_path / "missing-report"
    assert adapter.run(repository=root, expected_revision=revision, output_dir=output) == 2
    gate = json.loads((output / "gate-observation.json").read_text())["gate"]
    assert gate["decision"] == "ERROR" and gate["assessment_id"] is None
    assert gate["prevents_progression"] is False and len(calls) == 1
