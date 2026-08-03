import pytest

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)
from familyos_cli.plugins.builtin.health.records.health_record_registry import (
    HealthRecordRegistry,
)


def create_record() -> HealthRecord:
    return HealthRecord(
        id="record-001",
        profile_id="health-001",
        record_type="consultation",
        recorded_at="2026-08-03",
    )


def test_registry_registers_record() -> None:
    registry = HealthRecordRegistry()

    record = create_record()

    registry.register(
        record,
    )

    assert registry.contains(
        "record-001",
    )


def test_registry_returns_record() -> None:
    registry = HealthRecordRegistry()

    record = create_record()

    registry.register(
        record,
    )

    assert registry.get(
        "record-001",
    ) == record


def test_registry_rejects_duplicate_record() -> None:
    registry = HealthRecordRegistry()

    record = create_record()

    registry.register(
        record,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            record,
        )
