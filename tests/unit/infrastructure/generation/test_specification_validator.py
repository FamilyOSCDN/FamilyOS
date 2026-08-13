"""Tests for SpecificationValidator."""

from typing import Any

import pytest

from familyos_cli.infrastructure.generation.specification_validator import (
    SpecificationValidator,
)
from familyos_cli.shared.exceptions import ValidationError


def valid_specification() -> dict[str, Any]:
    """Return a valid project specification."""

    return {
        "project": {
            "directories": [
                "docs",
                "src",
            ],
            "files": [
                {
                    "destination": "README.md",
                    "template": "project/README.md.j2",
                },
            ],
        },
    }


def test_validate_valid_specification() -> None:
    """A valid specification should pass."""

    validator = SpecificationValidator()

    validator.validate(valid_specification())


def test_validate_missing_project() -> None:
    """Missing project should raise ValidationError."""

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate({})


def test_validate_missing_directories() -> None:
    """Missing directories should raise ValidationError."""

    specification = valid_specification()
    del specification["project"]["directories"]

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)


def test_validate_missing_files() -> None:
    """Missing files should raise ValidationError."""

    specification = valid_specification()
    del specification["project"]["files"]

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)


def test_validate_directories_must_be_list() -> None:
    """Directories must be a list."""

    specification = valid_specification()
    specification["project"]["directories"] = "docs"

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)


def test_validate_files_must_be_list() -> None:
    """Files must be a list."""

    specification = valid_specification()
    specification["project"]["files"] = "README.md"

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)


def test_validate_missing_destination() -> None:
    """Missing destination should raise ValidationError."""

    specification = valid_specification()

    del specification["project"]["files"][0]["destination"]

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)


def test_validate_missing_template() -> None:
    """Missing template should raise ValidationError."""

    specification = valid_specification()

    del specification["project"]["files"][0]["template"]

    validator = SpecificationValidator()

    with pytest.raises(ValidationError):
        validator.validate(specification)
