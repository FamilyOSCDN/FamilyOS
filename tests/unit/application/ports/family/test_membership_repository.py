"""Tests for the canonical MembershipRepository port."""

from __future__ import annotations

import inspect
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import MembershipRepository
from familyos_cli.domain.family import FamilyId, Membership
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


def test_membership_repository_is_abstract() -> None:
    assert inspect.isabstract(MembershipRepository)


def test_membership_repository_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        MembershipRepository()  # type: ignore[abstract]


def test_concrete_repository_can_implement_canonical_contract() -> None:
    class Repository(MembershipRepository):
        def __init__(self) -> None:
            self._memberships: dict[tuple[FamilyId, PersonId], Membership] = {}

        def save(self, membership: Membership) -> None:
            self._memberships[(membership.family_id, membership.person_id)] = membership

        def get(
            self,
            family_id: FamilyId,
            person_id: PersonId,
        ) -> Membership | None:
            return self._memberships.get((family_id, person_id))

    repository = Repository()
    membership = Membership.establish(_family_id(), _person_id())

    assert repository.get(membership.family_id, membership.person_id) is None
    repository.save(membership)
    assert repository.get(membership.family_id, membership.person_id) == membership


def test_membership_repository_exposes_only_canonical_repository_operations() -> None:
    public_operations = {
        name
        for name, member in inspect.getmembers(
            MembershipRepository,
            inspect.isfunction,
        )
        if not name.startswith("_")
    }

    assert public_operations == {"get", "save"}
