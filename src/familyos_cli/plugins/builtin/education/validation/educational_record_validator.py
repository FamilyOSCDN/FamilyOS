"""Educational record domain validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.models.educational_record import (
    EducationalRecord,
)


class EducationalRecordValidator:
    """Validate educational record business rules."""

    def validate(
        self,
        record: EducationalRecord,
    ) -> bool:
        """Validate educational record."""

        return bool(
            record.learner_id.strip()
            and record.course_id.strip()
            and record.result.strip()
        )
