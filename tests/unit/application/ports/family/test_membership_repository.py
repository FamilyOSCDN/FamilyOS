"""Tests for the canonical MembershipRepository temporal persistence port."""

from __future__ import annotations

import inspect
from datetime import UTC, datetime
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    MembershipRepository,
    MembershipTemporalFact,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipCreated,
    Membership,
)
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


def test_concrete_repository_accepts_entity_and_temporal_fact_atomically() -> None:
    class Repository(MembershipRepository):
        def __init__(self) -> None:
            self.membership: Membership | None = None
            self.fact: MembershipTemporalFact | None = None

        def save(
            self,
            membership: Membership,
            temporal_fact: MembershipTemporalFact,
        ) -> None:
            self.membership = membership
            self.fact = temporal_fact

        def get(
            self,
            family_id: FamilyId,
            person_id: PersonId,
        ) -> Membership | None:
            if self.membership is None:
                return None
            if (
                self.membership.family_id != family_id
                or self.membership.person_id != person_id
            ):
                return None
            return self.membership

    repository = Repository()
    membership = Membership.establish(_family_id(), _person_id())
    event = FamilyMembershipCreated(
        family_id=membership.family_id,
        person_id=membership.person_id,
        occurred_at=datetime(2026, 8, 28, 10, 0, tzinfo=UTC),
    )

    repository.save(membership, event)

    assert repository.get(membership.family_id, membership.person_id) == membership
    assert repository.fact == event


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
