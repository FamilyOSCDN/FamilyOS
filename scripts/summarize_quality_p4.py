"""Count P4 evidence against an explicit inventory of started observations."""

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.capture_quality_source import classify


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> Any:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object, parse_constant=_constant)


def _sample(sample: Any, folder: Path, phase: str) -> dict[str, Any] | None:
    if sample is None:
        return None
    raw: dict[str, bytes] = {}
    valid = True
    times: list[datetime] = []
    for name, arguments in (("head", ["rev-parse", "HEAD"]), ("status", ["status", "--porcelain=v1", "--untracked-files=all"])):
        command = sample[name]
        if command["command"] != ["git", *arguments]:
            raise ValueError("unexpected capture command")
        code = command["exit_code"]
        if code is not None and type(code) is not int:
            raise ValueError("invalid Git exit code")
        valid = valid and code == 0 and command["error"] is None
        for key in ("started_at", "finished_at"):
            timestamp = datetime.fromisoformat(command[key])
            if timestamp.tzinfo is None:
                raise ValueError("capture timestamps require a timezone")
            times.append(timestamp)
        for channel, suffix in (("stdout", ""), ("stderr", ".stderr")):
            ref = command[channel]
            filename = f"{name}-{phase}{suffix}"
            if ref["file"] != filename:
                raise ValueError("unexpected capture filename")
            data = (folder / filename).read_bytes()
            if hashlib.sha256(data).hexdigest() != ref["sha256"] or len(data) != ref["bytes"]:
                raise ValueError(f"capture integrity mismatch: {filename}")
            if channel == "stdout":
                raw[name] = data
    if times != sorted(times):
        raise ValueError("capture command timestamps are not ordered")
    started, finished = (datetime.fromisoformat(sample[key]) for key in ("started_at", "finished_at"))
    if started.tzinfo is None or finished.tzinfo is None or not started <= times[0] <= times[-1] <= finished:
        raise ValueError("invalid capture time window")
    head = raw["head"].strip().decode("ascii", errors="replace")
    valid = valid and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head) is not None
    actual = {"state": ("modified" if raw["status"] else "clean") if valid else "unavailable",
              "head_value": head if valid else None}
    if any(sample[key] != value for key, value in actual.items()):
        raise ValueError("capture state disagrees with raw Git evidence")
    return {**actual, "started_at": sample["started_at"], "finished_at": sample["finished_at"]}


def summarize(inventory: list[dict[str, Any]], *, root: Path) -> dict[str, Any]:
    """Missing/corrupt evidence remains unavailable, never a clean run."""
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in inventory:
        identity = {key: item[key] for key in ("run_id", "run_attempt", "event", "expected_revision")}
        if any(not isinstance(value, str) or not value for value in identity.values()):
            raise ValueError("inventory identity fields must be nonempty strings")
        key = identity["run_id"], identity["run_attempt"]
        if key in seen:
            raise ValueError("duplicate run/attempt in started-run inventory")
        seen.add(key)
        row: dict[str, Any] = {**identity, "capture_path": item.get("capture_path")}
        try:
            if item.get("capture_path") is None:
                raise ValueError("p4_artifact_unavailable")
            path = (root / item["capture_path"]).resolve()
            record = _json(path)
            if record["schema_version"] != "1.0.0" or record["kind"] != "quality-source-observation":
                raise ValueError("unsupported P4 schema")
            if any(record["identity"][key] != value for key, value in identity.items()):
                raise ValueError("P4 capture does not match inventory run/attempt/revision")
            before, after = (_sample(record[phase], path.parent, phase) for phase in ("before", "after"))
            if before is not None and after is not None and datetime.fromisoformat(before["finished_at"]) > datetime.fromisoformat(after["started_at"]):
                raise ValueError("before/after capture windows overlap or are reversed")
            measurement = classify(before, after, identity["expected_revision"])
            if record["measurement"] != measurement:
                raise ValueError("declared P4 measurement disagrees with retained evidence")
            row.update(measurement)
            row["observation_window"] = None if before is None or after is None else {
                "start": before["started_at"], "end": after["finished_at"],
                "semantics": "conservative global interval including capture and CLI overhead",
            }
        except (OSError, ValueError, TypeError, KeyError) as exc:
            row.update(eligible=False, triggered=None, state="unavailable", source_modified_before=False,
                       reasons=[str(exc)])
        rows.append(row)
    eligible = sum(row["eligible"] is True for row in rows)
    triggered = sum(row["triggered"] is True for row in rows)
    unavailable = [row for row in rows if row["state"] == "unavailable" or "unexpected_revision_before" in row["reasons"]]
    reasons: dict[str, int] = {}
    for row in unavailable:
        for reason in row["reasons"]:
            reasons[reason] = reasons.get(reason, 0) + 1
    return {"schema_version": "1.0.0", "started": len(rows), "eligible": eligible,
            "triggers": triggered,
            "frequency": {"numerator": triggered, "denominator": eligible, "ratio": triggered / eligible if eligible else None},
            "coverage": {"numerator": eligible, "denominator": len(rows), "ratio": eligible / len(rows) if rows else None},
            "unavailable_count": len(unavailable), "unavailable_reasons": reasons,
            "source_modified_before_count": sum(row["source_modified_before"] is True for row in rows),
            "unattributed_trigger_count": triggered, "attributions_by_tool_version_cause": [],
            "attribution_note": "No attribution inferred; independent reproduction and linked evidence are required.",
            "open_incidents": [{**row, "attribution": "unattributed"} for row in rows if row["triggered"] is True],
            "observations": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inventory = _json(args.inventory)
    if not isinstance(inventory, list):
        raise ValueError("started-run inventory must be an array")
    result = summarize(inventory, root=args.inventory.parent)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=True, allow_nan=False)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
