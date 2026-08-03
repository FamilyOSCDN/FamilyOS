import pytest

from familyos_cli.plugins.builtin.health.profiles.health_profile import (
    HealthProfile,
)


def test_health_profile_can_be_created() -> None:
    profile = HealthProfile(
        id="health-001",
        person_id="person-001",
    )

    assert profile.id == "health-001"
    assert profile.person_id == "person-001"
    assert profile.status == "active"


def test_health_profile_supports_metadata() -> None:
    profile = HealthProfile(
        id="health-001",
        person_id="person-001",
        metadata={
            "source": "family",
        },
    )

    assert profile.metadata["source"] == "family"


def test_health_profile_requires_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health profile id cannot be empty.",
    ):
        HealthProfile(
            id="",
            person_id="person-001",
        )


def test_health_profile_requires_person_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health profile person id cannot be empty.",
    ):
        HealthProfile(
            id="health-001",
            person_id="",
        )
