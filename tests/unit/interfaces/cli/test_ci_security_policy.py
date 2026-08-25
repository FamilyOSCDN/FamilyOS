"""Structural security contract for canonical CI automation."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

WORKFLOW_PATH = Path(".github/workflows/ci.yml")


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def _workflow() -> dict[object, object]:
    loaded = yaml.safe_load(_workflow_text())
    assert isinstance(loaded, dict)
    return loaded


def test_canonical_ci_uses_read_only_repository_permission() -> None:
    workflow = _workflow()

    permissions = workflow.get("permissions")

    assert permissions == {"contents": "read"}


def test_canonical_ci_does_not_use_pull_request_target() -> None:
    workflow = _workflow()

    triggers = workflow.get("on")

    if isinstance(triggers, dict):
        assert "pull_request_target" not in triggers

    assert "pull_request_target:" not in _workflow_text()


def test_canonical_ci_does_not_reference_repository_secrets() -> None:
    text = _workflow_text()

    assert "${{ secrets." not in text
    assert "secrets[" not in text


def test_canonical_ci_has_no_privileged_token_permissions() -> None:
    text = _workflow_text()

    forbidden_permissions = (
        "id-token: write",
        "packages: write",
        "contents: write",
        "deployments: write",
        "security-events: write",
    )

    for permission in forbidden_permissions:
        assert permission not in text


def test_canonical_ci_contains_no_release_publication_operation() -> None:
    text = _workflow_text().lower()

    forbidden_markers = (
        "pypi",
        "twine",
        "gh release",
        "create-release",
        "publish release",
        "release publication",
    )

    for marker in forbidden_markers:
        assert marker not in text


def test_canonical_ci_actions_are_pinned_to_commit_sha() -> None:
    text = _workflow_text()

    action_references = re.findall(
        r"^[ ]*uses:[ ]*([^#\n]+)",
        text,
        flags=re.MULTILINE,
    )

    assert action_references

    for reference in action_references:
        reference = reference.strip()

        if reference.startswith("./"):
            continue

        assert re.fullmatch(
            r"[^@\s]+@[0-9a-fA-F]{40}",
            reference,
        ), reference
