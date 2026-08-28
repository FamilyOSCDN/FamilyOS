"""Tests for canonical GetMembership application semantics."""

from __future__ import annotations

from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import GetMembership
from familyos_cli.application.ports.family import MembershipRepository
from familyos_cli.domain.family import FamilyId, Membership
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


class StubMembershipRepository(MembershipRepository):
    def __init__(self, membership: Membership | None) -> None:
        self.membership = membership
        self.requests: list[tuple[FamilyId, PersonId]] = []

    def save(self, membership: Membership, temporal_fact: object) -> None:
        self.membership = membership

    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        self.requests.append((family_id, person_id))

        if self.membership is None:
            return None

        if (
            self.membership.family_id != family_id
            or self.membership.person_id != person_id
        ):
            return None

        return self.membership


def test_get_membership_returns_canonical_membership_when_present() -> None:
    membership = Membership.establish(_family_id(), _person_id())
    repository = StubMembershipRepository(membership)

    result = GetMembership(repository).execute(_family_id(), _person_id())

    assert result == membership
    assert repository.requests == [(_family_id(), _person_id())]


def test_get_membership_returns_ended_membership_as_present() -> None:
    membership = Membership.establish(_family_id(), _person_id()).end()
    repository = StubMembershipRepository(membership)

    result = GetMembership(repository).execute(_family_id(), _person_id())

    assert result == membership


def test_get_membership_returns_none_for_ordinary_absence() -> None:
    repository = StubMembershipRepository(None)

    result = GetMembership(repository).execute(_family_id(), _person_id())

    assert result is None


def test_get_membership_propagates_repository_failure() -> None:
    class FailingRepository(MembershipRepository):
        def save(self, membership: Membership, temporal_fact: object) -> None:
            raise AssertionError("save must not be called")

        def get(
            self,
            family_id: FamilyId,
            person_id: PersonId,
        ) -> Membership | None:
            raise RuntimeError("persistence unavailable")

    with pytest.raises(RuntimeError, match="persistence unavailable"):
        GetMembership(FailingRepository()).execute(_family_id(), _person_id())


def test_get_membership_does_not_coerce_identifiers() -> None:
    class TypeCheckingRepository(MembershipRepository):
        def save(self, membership: Membership, temporal_fact: object) -> None:
            raise AssertionError("save must not be called")

        def get(
            self,
            family_id: FamilyId,
            person_id: PersonId,
        ) -> Membership | None:
            if not isinstance(family_id, FamilyId):
                raise TypeError("family_id must be a FamilyId")
            if not isinstance(person_id, PersonId):
                raise TypeError("person_id must be a PersonId")
            return None

    query = GetMembership(TypeCheckingRepository())

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        query.execute(cast(FamilyId, "family-001"), _person_id())

    with pytest.raises(TypeError, match="person_id must be a PersonId"):
        query.execute(_family_id(), cast(PersonId, "person-001"))
