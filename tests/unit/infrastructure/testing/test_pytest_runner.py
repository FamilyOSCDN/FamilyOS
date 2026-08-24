"""Tests for the structured subprocess-backed pytest runner."""

from __future__ import annotations

from pathlib import Path

import pytest
from familyos_cli.application.ports.testing.pytest_runner import (
    PytestRunnerPort,
)
from familyos_cli.infrastructure.testing.pytest_runner import PytestRunner

from familyos_cli.application.testing import PytestExecutionResult


def test_pytest_runner_implements_canonical_port() -> None:
    runner = PytestRunner()

    assert isinstance(runner, PytestRunnerPort)


def test_pytest_runner_returns_structured_passing_result(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "def test_passes():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(test_file,),
    )

    assert isinstance(result, PytestExecutionResult)
    assert result.exit_code == 0
    assert result.discovered == 1
    assert result.executed == 1
    assert result.passed == 1
    assert result.failed == 0
    assert result.skipped == 0
    assert result.errors == 0
    assert result.duration_seconds >= 0.0
    assert result.diagnostic is None


def test_pytest_runner_returns_structured_failure(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "def test_fails():\n"
        "    assert False\n",
        encoding="utf-8",
    )

    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(test_file,),
    )

    assert result.exit_code == 1
    assert result.discovered == 1
    assert result.executed == 1
    assert result.passed == 0
    assert result.failed == 1
    assert result.skipped == 0
    assert result.errors == 0
    assert result.duration_seconds >= 0.0


def test_pytest_runner_counts_skipped_test_once(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "import pytest\n\n"
        "@pytest.mark.skip(reason='contract')\n"
        "def test_skipped():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(test_file,),
    )

    assert result.exit_code == 0
    assert result.discovered == 1
    assert result.executed == 1
    assert result.passed == 0
    assert result.failed == 0
    assert result.skipped == 1
    assert result.errors == 0


def test_pytest_runner_classifies_setup_error_once(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "import pytest\n\n"
        "@pytest.fixture\n"
        "def broken_fixture():\n"
        "    raise RuntimeError('fixture failed')\n\n"
        "def test_error(broken_fixture):\n"
        "    assert broken_fixture\n",
        encoding="utf-8",
    )

    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(test_file,),
    )

    assert result.exit_code == 1
    assert result.discovered == 1
    assert result.executed == 1
    assert result.passed == 0
    assert result.failed == 0
    assert result.skipped == 0
    assert result.errors == 1


def test_pytest_runner_does_not_double_count_teardown_error(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "import pytest\n\n"
        "@pytest.fixture\n"
        "def broken_teardown():\n"
        "    yield\n"
        "    raise RuntimeError('teardown failed')\n\n"
        "def test_body_passes(broken_teardown):\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(test_file,),
    )

    assert result.exit_code == 1
    assert result.discovered == 1
    assert result.executed == 1
    assert result.passed == 0
    assert result.failed == 0
    assert result.skipped == 0
    assert result.errors == 1


def test_pytest_runner_preserves_no_tests_collected_exit_code(
    tmp_path: Path,
) -> None:
    result = PytestRunner().run(
        project_root=tmp_path,
        test_paths=(),
    )

    assert result.exit_code == pytest.ExitCode.NO_TESTS_COLLECTED
    assert result.discovered == 0
    assert result.executed == 0
    assert result.passed == 0
    assert result.failed == 0
    assert result.skipped == 0
    assert result.errors == 0


def test_pytest_runner_rejects_test_path_outside_project_root(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    outside = tmp_path / "outside.py"
    outside.write_text(
        "def test_outside():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="test path must resolve inside project root",
    ):
        PytestRunner().run(
            project_root=project_root,
            test_paths=(outside,),
        )
