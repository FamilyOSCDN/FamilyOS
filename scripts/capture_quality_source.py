"""Retain additive Git source observations without running Quality tools."""

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _write_json(path: Path, value: dict[str, Any], *, exclusive: bool = True) -> None:
    with path.open("x" if exclusive else "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True, allow_nan=False)
        stream.write("\n")


def _load(path: Path) -> dict[str, Any]:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"P4 record must be an object: {path.name}")
    return value


def _git(repository: Path, output: Path, phase: str, name: str, arguments: list[str]) -> tuple[dict[str, Any], bytes]:
    command = ["git", *arguments]
    started_at = _now()
    exit_code: int | None = None
    error: str | None = None
    stdout = stderr = b""
    try:
        completed = subprocess.run(command, cwd=repository, capture_output=True, timeout=30, check=False)
        exit_code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, bytes) else b""
        stderr = exc.stderr if isinstance(exc.stderr, bytes) else b""
        error = "Git capture timed out after 30 seconds"
    except OSError as exc:
        error = str(exc)
    finished_at = _now()
    files: dict[str, dict[str, Any]] = {}
    for channel, data, filename in (
        ("stdout", stdout, f"{name}-{phase}"),
        ("stderr", stderr, f"{name}-{phase}.stderr"),
    ):
        with (output / filename).open("xb") as stream:
            stream.write(data)
        files[channel] = {"file": filename, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    record = {"command": command, "started_at": started_at, "finished_at": finished_at,
              "exit_code": exit_code, "error": error, **files}
    # One escaped JSON line cannot turn a filename into a GitHub workflow command.
    print(json.dumps({"p4_phase": phase, "capture": name, **record,
                      "stdout_escaped": stdout.decode("utf-8", errors="backslashreplace"),
                      "stderr_escaped": stderr.decode("utf-8", errors="backslashreplace")}, ensure_ascii=True))
    return record, stdout


def _sample(repository: Path, output: Path, phase: str) -> dict[str, Any]:
    started_at = _now()
    head, raw_head = _git(repository, output, phase, "head", ["rev-parse", "HEAD"])
    status, raw_status = _git(repository, output, phase, "status", ["status", "--porcelain=v1", "--untracked-files=all"])
    head_value = raw_head.strip().decode("ascii", errors="replace")
    valid = all(item["exit_code"] == 0 and item["error"] is None for item in (head, status))
    valid = valid and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head_value) is not None
    return {"started_at": started_at, "finished_at": _now(), "head": head, "status": status,
            "head_value": head_value if valid else None,
            "state": ("modified" if raw_status else "clean") if valid else "unavailable"}


def classify(before: dict[str, Any] | None, after: dict[str, Any] | None, expected_revision: str) -> dict[str, Any]:
    """Keep unavailable and pre-existing changes out of the P4 denominator."""
    reasons: list[str] = []
    for phase, sample in (("before", before), ("after", after)):
        if sample is None:
            reasons.append(f"{phase}_missing")
        elif sample["state"] == "unavailable":
            reasons.append(f"{phase}_git_unavailable")
    if before is not None and before["state"] != "unavailable":
        if before["state"] == "modified":
            reasons.append("source_modified_before")
        if before["head_value"] != expected_revision:
            reasons.append("unexpected_revision_before")
    eligible = not reasons
    triggered: bool | None = None
    state = "unavailable"
    if before is not None and after is not None and all(sample["state"] != "unavailable" for sample in (before, after)):
        state = "modified" if "modified" in (before["state"], after["state"]) or before["head_value"] != after["head_value"] else "clean"
    if eligible and before is not None and after is not None:
        triggered = after["state"] == "modified" or before["head_value"] != after["head_value"]
    return {"eligible": eligible, "triggered": triggered, "reasons": reasons,
            "state": state,
            "source_modified_before": before is not None and before["state"] == "modified"}


def _correlation(repository: Path, expected_revision: str, quality_output: Path | None) -> dict[str, Any]:
    """Retain durations as unanchored observations, never as tool attribution."""
    if quality_output is None:
        return {"available": False, "reason": "quality_output_not_supplied", "checks": []}
    try:
        # Lazy imports let raw Git capture work even after dependency setup fails.
        from familyos_cli.domain.quality import QualityTarget
        from scripts.quality_ci_report import read_report

        report_path = quality_output / "quality-report.json"
        result = read_report(report_path, QualityTarget(
            target_type="repository", identifier="familyos-cli", path=str(repository), revision=expected_revision,
        ))
        execution = _load(quality_output / "execution.json")
        if execution.get("revision") != expected_revision or not isinstance(execution.get("report_accepted"), bool):
            raise ValueError("Quality execution identity or acceptance is unavailable")
        return {"available": True, "report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
                "report_accepted": execution["report_accepted"],
                "timing_semantics": "durations_only; no executor start timestamps or inferred culprit",
                "checks": [{"check_id": str(check.check_id), "duration_seconds": check.duration_seconds,
                            "tools": [{"tool": item.tool, "version": item.tool_version} for item in check.evidence if item.tool is not None]}
                           for check in result.check_results]}
    except Exception as exc:
        return {"available": False, "reason": str(exc), "checks": []}


def capture(
    *, phase: str, repository: Path, expected_revision: str, output_dir: Path,
    run_id: str, run_attempt: str, event: str, quality_output: Path | None = None,
    quality_step_outcome: str | None = None,
) -> int:
    """Capture once into fresh sidecar files; preserve earlier evidence."""
    try:
        if phase not in ("before", "after"):
            raise ValueError("P4 phase must be before or after")
        repository, output_dir = repository.resolve(), output_dir.resolve()
        if output_dir.is_relative_to(repository):
            raise ValueError("P4 output must be outside the source checkout")
        if quality_output is not None:
            quality_output = quality_output.resolve()
            if output_dir.is_relative_to(quality_output) or quality_output.is_relative_to(output_dir):
                raise ValueError("P4 and Quality evidence directories must be disjoint")
        identity = {"run_id": run_id, "run_attempt": run_attempt, "event": event,
                    "repository": str(repository), "expected_revision": expected_revision}
        context_path = output_dir / "context.json"
        if phase == "before" or not output_dir.exists():
            output_dir.mkdir()
            _write_json(context_path, {"identity": identity, "created_at": _now(),
                                      "environment": {"python": platform.python_version(), "platform": platform.platform()}})
        context = _load(context_path)
        if context.get("identity") != identity:
            raise ValueError("P4 evidence belongs to another run, attempt or revision")
        sample = _sample(repository, output_dir, phase)
        _write_json(output_dir / f"capture-{phase}.json", sample)
        before_path, after_path = output_dir / "capture-before.json", output_dir / "capture-after.json"
        before = _load(before_path) if before_path.is_file() else None
        after = _load(after_path) if after_path.is_file() else None
        window = None if before is None or after is None else {
            "start": before["started_at"], "end": after["finished_at"],
            "semantics": "conservative global interval including capture and CLI overhead",
        }
        summary = {"schema_version": "1.0.0", "kind": "quality-source-observation", **context,
                   "before": before, "after": after, "measurement": classify(before, after, expected_revision),
                   "observation_window": window, "quality_step_outcome": quality_step_outcome,
                   "correlation": _correlation(repository, expected_revision, quality_output) if phase == "after" else None,
                   "attribution": {"status": "unattributed", "tool": None, "version": None, "cause": None, "evidence": []}}
        _write_json(output_dir / "p4-capture.json", summary, exclusive=False)
        print(json.dumps({"p4_measurement": summary["measurement"], "run": identity}, ensure_ascii=True))
        if sample["state"] == "unavailable":
            print("::warning::P4 Git measurement unavailable; see captured return codes and diagnostics.")
        return 0
    except Exception as exc:
        print("::warning::P4 evidence capture failed; this is not a clean-source observation.")
        print(json.dumps({"p4_capture_error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("before", "after"), required=True)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--expected-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-attempt", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--quality-output", type=Path)
    parser.add_argument("--quality-step-outcome")
    args = parser.parse_args()
    return capture(**vars(args))


if __name__ == "__main__":
    raise SystemExit(main())
