"""The governance denominator comes from started runs, including missing proofs."""

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from scripts.capture_quality_source import capture
from scripts.summarize_quality_p4 import summarize


@pytest.fixture
def measured_runs(tmp_path: Path) -> tuple[Path, list[dict[str, Any]]]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "tracked").write_text("clean")
    subprocess.run(["git", "init", "-q"], cwd=source, check=True)
    subprocess.run(["git", "add", "tracked"], cwd=source, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], cwd=source, check=True)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    inventory: list[dict[str, Any]] = []
    for run_id in ("clean", "modified", "lost", "preexisting"):
        folder = tmp_path / run_id
        identity = {"run_id": run_id, "run_attempt": "1", "event": "push", "expected_revision": revision}
        inventory.append({**identity, "capture_path": None if run_id == "lost" else f"{run_id}/p4-capture.json"})
        if run_id == "lost":
            continue
        assert capture(phase="before", repository=source, output_dir=folder, run_id=run_id,
                       run_attempt="1", event="push", expected_revision=revision) == 0
        if run_id == "modified":
            (source / "tracked").write_text("modified")
        assert capture(phase="after", repository=source, output_dir=folder, run_id=run_id,
                       run_attempt="1", event="push", expected_revision=revision) == 0
    return tmp_path, inventory


def test_frequency_coverage_and_unknowns_are_separate(measured_runs: tuple[Path, list[dict[str, Any]]]) -> None:
    root, inventory = measured_runs
    result = summarize(inventory, root=root)
    assert result["frequency"] == {"numerator": 1, "denominator": 2, "ratio": 0.5}
    assert result["coverage"] == {"numerator": 2, "denominator": 4, "ratio": 0.5}
    assert result["unavailable_count"] == 1
    assert result["unavailable_reasons"] == {"p4_artifact_unavailable": 1}
    assert result["source_modified_before_count"] == 1
    assert result["unattributed_trigger_count"] == 1
    assert result["attributions_by_tool_version_cause"] == []
    assert result["open_incidents"][0]["run_id"] == "modified"


@pytest.mark.parametrize("tamper", ["bytes", "declared-clean", "run", "command", "filename", "time"])
def test_bad_evidence_is_excluded_instead_of_counted_clean(measured_runs: tuple[Path, list[dict[str, Any]]], tamper: str) -> None:
    root, inventory = measured_runs
    folder = root / "clean"
    record_path = folder / "p4-capture.json"
    record = json.loads(record_path.read_text())
    if tamper == "bytes":
        (folder / "status-after").write_bytes(b" M tracked\n")
    elif tamper == "declared-clean":
        record["measurement"]["triggered"] = True
    elif tamper == "run":
        record["identity"]["run_id"] = "different"
    elif tamper == "command":
        record["after"]["status"]["command"][-1] = "--untracked-files=normal"
    elif tamper == "filename":
        record["after"]["status"]["stdout"]["file"] = "../other"
    else:
        record["after"]["finished_at"] = "2000-01-01T00:00:00+00:00"
    record_path.write_text(json.dumps(record))
    result = summarize(inventory[:1], root=root)
    assert result["eligible"] == 0 and result["unavailable_count"] == 1
    assert result["frequency"]["ratio"] is None


def test_lost_measurements_and_empty_inventory_never_produce_zero_frequency(tmp_path: Path) -> None:
    empty = summarize([], root=tmp_path)
    assert empty["frequency"]["ratio"] is None and empty["coverage"]["ratio"] is None
    missing = summarize([{"run_id": "1", "run_attempt": "1", "event": "push", "expected_revision": "a" * 40, "capture_path": None}], root=tmp_path)
    assert missing["frequency"] == {"numerator": 0, "denominator": 0, "ratio": None}
    assert missing["coverage"] == {"numerator": 0, "denominator": 1, "ratio": 0.0}


def test_duplicate_inventory_cannot_inflate_coverage(measured_runs: tuple[Path, list[dict[str, Any]]]) -> None:
    root, inventory = measured_runs
    with pytest.raises(ValueError, match="duplicate run/attempt"):
        summarize([inventory[0], inventory[0]], root=root)
