"""Specification validator."""

from typing import Any

from familyos_cli.shared.exceptions import ValidationError


class SpecificationValidator:
    """Validate project specifications."""

    def validate(self, specification: dict[str, Any]) -> None:
        """Validate a project specification."""

        if "project" not in specification:
            raise ValidationError(
                "Missing required section: 'project'."
            )

        project = specification["project"]

        if "directories" not in project:
            raise ValidationError(
                "Missing required field: 'project.directories'."
            )

        if "files" not in project:
            raise ValidationError(
                "Missing required field: 'project.files'."
            )

        if not isinstance(project["directories"], list):
            raise ValidationError(
                "'project.directories' must be a list."
            )

        if not isinstance(project["files"], list):
            raise ValidationError(
                "'project.files' must be a list."
            )

        for index, file in enumerate(project["files"]):
            if "destination" not in file:
                raise ValidationError(
                    f"Missing 'destination' in file #{index}."
                )

            if "template" not in file:
                raise ValidationError(
                    f"Missing 'template' in file #{index}."
                )