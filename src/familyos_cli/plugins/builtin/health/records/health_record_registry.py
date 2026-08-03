"""Health record registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)


class HealthRecordRegistry:
    """Registry of health records."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._records: dict[str, HealthRecord] = {}

    def register(
        self,
        record: HealthRecord,
    ) -> None:
        """Register health record."""

        if record.id in self._records:
            raise ValueError(
                f"Health record '{record.id}' already registered.",
            )

        self._records[
            record.id
        ] = record

    def get(
        self,
        record_id: str,
    ) -> HealthRecord:
        """Return health record."""

        try:
            return self._records[
                record_id
            ]
        except KeyError as error:
            raise ValueError(
                f"Health record '{record_id}' not found.",
            ) from error

    def contains(
        self,
        record_id: str,
    ) -> bool:
        """Return whether record exists."""

        return record_id in self._records

    def list(
        self,
    ) -> tuple[HealthRecord, ...]:
        """Return all records."""

        return tuple(
            self._records.values(),
        )

    def clear(
        self,
    ) -> None:
        """Clear registry."""

        self._records.clear()
