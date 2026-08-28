"""In-memory adapter for the canonical Family repository port."""

from threading import Lock

from familyos_cli.application.ports.family import (
    FamilyConflictError,
    FamilyRepository,
)
from familyos_cli.domain.family import Family, FamilyId


class InMemoryFamilyRepository(FamilyRepository):
    """Store canonical Families in process memory by FamilyId."""

    def __init__(self) -> None:
        self._families: dict[FamilyId, Family] = {}
        self._lock = Lock()

    def save(self, family: Family) -> None:
        """Atomically establish the Family without replacing its identity."""

        with self._lock:
            if family.family_id in self._families:
                raise FamilyConflictError(
                    f"Family '{family.family_id}' already exists"
                )

            self._families[family.family_id] = family

    def get(self, family_id: FamilyId) -> Family | None:
        """Return the Family associated with FamilyId, or canonical absence."""

        with self._lock:
            return self._families.get(family_id)
