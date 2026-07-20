"""FamilyOS CLI exceptions."""

from familyos_cli.shared.exceptions.familyos_error import FamilyOSError
from familyos_cli.shared.exceptions.project_already_exists_error import (
    ProjectAlreadyExistsError,
)
from familyos_cli.shared.exceptions.specification_error import (
    SpecificationError,
)
from familyos_cli.shared.exceptions.specification_not_found_error import (
    SpecificationNotFoundError,
)
from familyos_cli.shared.exceptions.template_not_found_error import (
    TemplateNotFoundError,
)
from familyos_cli.shared.exceptions.validation_error import (
    ValidationError,
)

__all__ = [
    "FamilyOSError",
    "ProjectAlreadyExistsError",
    "SpecificationError",
    "SpecificationNotFoundError",
    "TemplateNotFoundError",
    "ValidationError",
]