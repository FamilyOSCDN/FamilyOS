"""Health validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)
from familyos_cli.plugins.builtin.health.validation.health_validation_result import (
    HealthValidationResult,
)


class HealthValidator:
    """Validate health domain objects."""

    def validate_record(
        self,
        record: HealthRecord,
    ) -> HealthValidationResult:
        """Validate health record."""

        errors: list[str] = []

        if not record.profile_id:
            errors.append(
                "Health record profile id is required.",
            )

        if not record.record_type:
            errors.append(
                "Health record type is required.",
            )

        if not record.recorded_at:
            errors.append(
                "Health record date is required.",
            )

        if errors:
            return HealthValidationResult.failure(
                tuple(errors),
            )

        return HealthValidationResult.success()
