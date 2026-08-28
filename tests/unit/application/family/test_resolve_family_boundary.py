"""Tests for the canonical ResolveFamilyBoundary application query."""

from __future__ import annotations

from familyos_cli.application.family import ResolveFamilyBoundary
from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import Family, FamilyId


class RecordingFamilyRepository(FamilyRepository):
    """Minimal repository test double exposing only the Family port contract."""

    def __init__(self, families: tuple[Family, ...] = ()) -> None:
        self._families = {family.family_id: family for family in families}
        self.get_calls: list[FamilyId] = []

    def save(self, family: Family) -> None:
        self._families[family.family_id] = family

    def get(self, family_id: FamilyId) -> Family | None:
        self.get_calls.append(family_id)
        return self._families.get(family_id)


def test_resolve_family_boundary_uses_only_family_repository_boundary() -> None:
    family_id = FamilyId.generate()
    repository = RecordingFamilyRepository((Family(family_id),))
    use_case = ResolveFamilyBoundary(repository)

    resolved = use_case.execute(family_id)

    assert resolved == family_id
    assert repository.get_calls == [family_id]


def test_resolve_family_boundary_identity_is_the_canonical_family_id() -> None:
    family_id = FamilyId.generate()
    repository = RecordingFamilyRepository((Family(family_id),))

    resolved = ResolveFamilyBoundary(repository).execute(family_id)

    assert isinstance(resolved, FamilyId)
    assert resolved is family_id


def test_resolve_family_boundary_returns_absence_for_unknown_family() -> None:
    family_id = FamilyId.generate()
    repository = RecordingFamilyRepository()

    resolved = ResolveFamilyBoundary(repository).execute(family_id)

    assert resolved is None
    assert repository.get_calls == [family_id]


def test_distinct_families_resolve_to_distinct_boundaries() -> None:
    first_id = FamilyId.generate()
    second_id = FamilyId.generate()
    repository = RecordingFamilyRepository(
        (
            Family(first_id),
            Family(second_id),
        )
    )
    use_case = ResolveFamilyBoundary(repository)

    first_boundary = use_case.execute(first_id)
    second_boundary = use_case.execute(second_id)

    assert first_boundary == first_id
    assert second_boundary == second_id
    assert first_boundary != second_boundary


def test_boundary_resolution_does_not_require_membership_or_relationship_state() -> (
    None
):
    family_id = FamilyId.generate()
    repository = RecordingFamilyRepository((Family(family_id),))

    resolved = ResolveFamilyBoundary(repository).execute(family_id)

    assert resolved == family_id
