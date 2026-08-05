"""Finance account statuses."""

from enum import StrEnum


class AccountStatus(StrEnum):
    """Supported account lifecycle states."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"
