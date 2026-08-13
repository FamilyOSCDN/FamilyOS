"""Tests for DocumentProfile."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)


def create_profile(
    **overrides: str,
) -> DocumentProfile:
    """Create a document profile for tests."""

    values = {
        "id": "documents.profile.basic",
        "name": "Basic Documents Profile",
        "version": "1.0.0",
        "level": "BASIC",
    }
    values.update(
        overrides,
    )

    return DocumentProfile(
        id=values["id"],
        name=values["name"],
        version=values["version"],
        level=values["level"],
    )


def test_document_profile_can_be_created() -> None:
    """Document profile stores values."""

    profile = DocumentProfile(
        id="documents.profile.family",
        name="Family Documents Profile",
        version="1.0.0",
        level="STANDARD",
        description=(
            "Document profile for family environments."
        ),
    )

    assert profile.id == "documents.profile.family"
    assert profile.name == "Family Documents Profile"
    assert profile.version == "1.0.0"
    assert profile.level == "STANDARD"
    assert profile.description == (
        "Document profile for family environments."
    )


def test_document_profile_description_is_optional() -> None:
    """Description defaults to empty."""

    profile = create_profile()

    assert profile.description == ""


def test_document_profile_is_immutable() -> None:
    """Document profiles cannot be modified."""

    profile = create_profile()

    with pytest.raises(FrozenInstanceError):
        profile.level = "CRITICAL"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Document profile id cannot be empty.",
        ),
        (
            "name",
            "Document profile name cannot be empty.",
        ),
        (
            "version",
            "Document profile version cannot be empty.",
        ),
        (
            "level",
            "Document profile level cannot be empty.",
        ),
    ],
)
def test_document_profile_rejects_empty_required_fields(
    field: str,
    message: str,
) -> None:
    """Required document profile fields cannot be empty."""

    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_profile(
            **{field: "   "},
        )


@pytest.mark.parametrize(
    "level",
    [
        "BASIC",
        "STANDARD",
        "SENSITIVE",
        "CRITICAL",
        "basic",
        "standard",
        "sensitive",
        "critical",
    ],
)
def test_document_profile_accepts_supported_levels(
    level: str,
) -> None:
    """Supported document levels are accepted."""

    profile = create_profile(
        level=level,
    )

    assert profile.level == level


def test_document_profile_rejects_unsupported_level() -> None:
    """Unknown document profile levels are rejected."""

    with pytest.raises(
        ValueError,
        match="Unsupported document profile level: UNKNOWN.",
    ):
        create_profile(
            level="UNKNOWN",
        )
