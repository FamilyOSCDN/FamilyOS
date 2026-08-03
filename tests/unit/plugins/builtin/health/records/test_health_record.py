import pytest

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)


def test_health_record_can_be_created() -> None:
    record = HealthRecord(
        id="record-001",
        profile_id="health-001",
        record_type="consultation",
        recorded_at="2026-08-03",
    )

    assert record.id == "record-001"
    assert record.profile_id == "health-001"
    assert record.record_type == "consultation"
    assert record.recorded_at == "2026-08-03"


def test_health_record_supports_metadata() -> None:
    record = HealthRecord(
        id="record-001",
        profile_id="health-001",
        record_type="measurement",
        recorded_at="2026-08-03",
        metadata={
            "source": "doctor",
        },
    )

    assert record.metadata["source"] == "doctor"


def test_health_record_requires_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health record id cannot be empty.",
    ):
        HealthRecord(
            id="",
            profile_id="health-001",
            record_type="consultation",
            recorded_at="2026-08-03",
        )


def test_health_record_requires_profile_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health record profile id cannot be empty.",
    ):
        HealthRecord(
            id="record-001",
            profile_id="",
            record_type="consultation",
            recorded_at="2026-08-03",
        )
