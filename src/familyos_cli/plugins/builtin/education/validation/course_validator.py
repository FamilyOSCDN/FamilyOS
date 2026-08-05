"""Course domain validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.models.course import (
    Course,
)


class CourseValidator:
    """Validate course business rules."""

    def validate(
        self,
        course: Course,
    ) -> bool:
        """Validate course."""

        return bool(
            course.title.strip()
            and course.category.strip()
        )
