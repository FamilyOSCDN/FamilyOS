"""Reproduce canonical Quality reporting with traceable CI artifacts."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from familyos_cli.application.quality import QualityAssessmentExecutionResult
from familyos_cli.domain.quality import QualityTarget
from scripts.quality_ci_report import read_report, render_summary


def checked_revision(repository: Path, expected: str) -> str:
    """Reject a different or modified source before accepting its evidence."""
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repository, text=True, stderr=subprocess.PIPE,
    ).strip()
    if revision != expected:
        raise ValueError("checked Git HEAD does not match expected revision")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=repository, text=True, stderr=subprocess.PIPE,
    )
    if status:
        raise ValueError("Quality CI requires clean tracked and non-ignored source")
    return revision


def run(
    *, repository: Path, expected_revision: str, output_dir: Path,
    summary_path: Path | None = None,
) -> int:
    """Invoke the public CLI once, retaining its result and operational failures."""
    try:
        repository = repository.resolve()
        output_dir = output_dir.resolve()
        if output_dir.is_relative_to(repository):
            raise ValueError("Quality CI output must be outside the source checkout")
        if summary_path is not None:
            summary_path = summary_path.resolve()
            if summary_path.is_relative_to(repository) or summary_path.is_relative_to(output_dir):
                raise ValueError("Quality CI summary must be outside source and artifacts")
        output_dir.mkdir()
    except Exception as exc:
        print(f"Quality CI artifact initialization failed: {exc}", file=sys.stderr)
        return 2

    revision: str | None = None
    command: list[str] = []
    cli_exit_code: int | None = None
    adapter_exit_code = 2
    adapter_error: str | None = None
    result: QualityAssessmentExecutionResult | None = None
    try:
        with (output_dir / "stdout.log").open("wb") as stdout, (output_dir / "stderr.log").open("wb") as stderr:
            revision = checked_revision(repository, expected_revision)
            command = [
                "familyos", "quality", "report", "--target-type", "repository",
                "--identifier", "familyos-cli", "--path", str(repository),
                "--revision", revision, "--format", "json",
                "--output", str(output_dir / "quality-report.json"),
            ]
            completed = subprocess.run(command, cwd=repository, stdout=stdout, stderr=stderr, check=False)
            cli_exit_code = completed.returncode
        if cli_exit_code not in (0, 1, 2):
            raise ValueError(f"unexpected Quality CLI exit code: {cli_exit_code}")
        checked_revision(repository, expected_revision)
        result = read_report(
            output_dir / "quality-report.json",
            QualityTarget(target_type="repository", identifier="familyos-cli", path=str(repository), revision=revision),
        )
        adapter_exit_code = cli_exit_code
    except Exception as exc:
        adapter_error = str(exc)

    try:
        summary = render_summary(
            result, revision=revision, cli_exit_code=cli_exit_code,
            adapter_exit_code=adapter_exit_code, adapter_error=adapter_error,
        )
        (output_dir / "quality-summary.md").write_text(summary, encoding="utf-8")
        if summary_path is not None:
            with summary_path.open("a", encoding="utf-8") as stream:
                stream.write(summary)
    except Exception as exc:
        adapter_exit_code = 2
        adapter_error = f"{adapter_error + '; ' if adapter_error else ''}Summary output failed: {exc}"
    record = {
        "schema_version": "1.0.0", "revision": revision, "command": command,
        "cli_exit_code": cli_exit_code, "adapter_exit_code": adapter_exit_code,
        "report_accepted": result is not None, "adapter_error": adapter_error,
    }
    try:
        (output_dir / "execution.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        adapter_exit_code = 2
        adapter_error = f"Execution record output failed: {exc}"
    if adapter_error is not None:
        print(f"Quality CI adapter failed: {adapter_error}", file=sys.stderr)
    return adapter_exit_code


def main(argv: list[str] | None = None) -> int:
    """Parse explicit CI transport inputs; the Quality CLI owns execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--expected-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    return run(
        repository=args.repository, expected_revision=args.expected_revision,
        output_dir=args.output_dir, summary_path=args.summary,
    )


if __name__ == "__main__":
    raise SystemExit(main())
