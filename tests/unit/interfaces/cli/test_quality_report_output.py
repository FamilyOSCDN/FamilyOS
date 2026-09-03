"""Atomic file replacement and failure preservation for Quality reports."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from unittest.mock import Mock

import pytest

from familyos_cli.interfaces.cli import quality_report_output as output


def test_relative_destination_receives_exact_utf8_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    destination = Path("quality.json")
    destination.write_text("previous", encoding="utf-8")
    rendered = '{"message": "échec"}\n'

    output.write_quality_report(destination, rendered)

    assert destination.read_bytes() == rendered.encode("utf-8")
    assert list(tmp_path.iterdir()) == [tmp_path / destination]


def test_destination_symlink_is_replaced_without_modifying_referent(tmp_path: Path) -> None:
    referent = tmp_path / "other.json"
    referent.write_text("other report", encoding="utf-8")
    destination = tmp_path / "quality.json"
    destination.symlink_to(referent)

    output.write_quality_report(destination, "{}\n")

    assert destination.read_text() == "{}\n"
    assert not destination.is_symlink()
    assert referent.read_text() == "other report"


def test_success_does_not_remove_a_recreated_temporary_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "quality.json"
    recreated: list[Path] = []
    original_replace = Path.replace

    def replace(source: Path, target: Path) -> Path:
        result = original_replace(source, target)
        source.write_text("unrelated", encoding="utf-8")
        recreated.append(source)
        return result

    monkeypatch.setattr(Path, "replace", replace)

    output.write_quality_report(destination, "{}\n")

    assert destination.read_text(encoding="utf-8") == "{}\n"
    assert len(recreated) == 1
    assert recreated[0].read_text(encoding="utf-8") == "unrelated"


@pytest.mark.parametrize("stage", ("write", "replace"))
def test_write_failures_preserve_existing_artifact_and_remove_temporary_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stage: str,
) -> None:
    destination = tmp_path / "quality.json"
    destination.write_text("previous", encoding="utf-8")
    error = OSError(f"{stage} unavailable")
    if stage == "replace":
        monkeypatch.setattr(Path, "replace", Mock(side_effect=error))
    else:
        original = NamedTemporaryFile

        def failing_stream(**kwargs: Any) -> Any:
            stream = original(**kwargs)
            monkeypatch.setattr(stream, "write", Mock(side_effect=error))
            return stream

        monkeypatch.setattr(output, "NamedTemporaryFile", failing_stream)

    with pytest.raises(OSError) as failure:
        output.write_quality_report(destination, "{}\n")

    assert failure.value is error
    assert destination.read_text() == "previous"
    assert list(tmp_path.iterdir()) == [destination]


def test_invalid_utf8_does_not_touch_destination(tmp_path: Path) -> None:
    destination = tmp_path / "quality.json"
    destination.write_text("previous", encoding="utf-8")
    with pytest.raises(UnicodeError):
        output.write_quality_report(destination, "\ud800")
    assert destination.read_text() == "previous"
    assert list(tmp_path.iterdir()) == [destination]


def test_missing_parent_is_not_created(tmp_path: Path) -> None:
    destination = tmp_path / "absent" / "quality.json"
    with pytest.raises(FileNotFoundError):
        output.write_quality_report(destination, "{}\n")
    assert not destination.parent.exists()
