"""Tests for the in-memory canonical Relationship repository adapter."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    RelationshipConflictError,
    RelationshipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    Relationship,
    RelationshipState,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId
from familyos_cli.infrastructure.family import InMemoryRelationshipRepository


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _low_person_id() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _high_person_id() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def _key(
    relationship: Relationship,
) -> tuple[FamilyId, PersonId, PersonId, RelationshipType]:
    return (
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
    )


def test_repository_implements_canonical_port() -> None:
    assert isinstance(InMemoryRelationshipRepository(), RelationshipRepository)


def test_initial_established_save_then_get_returns_relationship() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    repository = InMemoryRelationshipRepository()

    repository.save(relationship)

    assert repository.get(*_key(relationship)) == relationship


def test_get_returns_none_for_absent_canonical_key() -> None:
    repository = InMemoryRelationshipRepository()

    assert repository.get(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    ) is None


def test_initial_save_rejects_ended_state() -> None:
    ended = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    ).end()
    repository = InMemoryRelationshipRepository()

    with pytest.raises(
        RelationshipConflictError,
        match="Initial Relationship persistence requires ESTABLISHED state",
    ):
        repository.save(ended)

    assert repository.get(*_key(ended)) is None


def test_duplicate_established_save_is_conflict_and_does_not_replace() -> None:
    first = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    second = Relationship.establish(
        first.family_id,
        first.source_person_id,
        first.target_person_id,
        first.relationship_type,
    )
    repository = InMemoryRelationshipRepository()

    repository.save(first)

    with pytest.raises(RelationshipConflictError):
        repository.save(second)

    assert repository.get(*_key(first)) is first


def test_save_accepts_only_established_to_ended_successor() -> None:
    established = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    ended = established.end()
    repository = InMemoryRelationshipRepository()

    repository.save(established)
    repository.save(ended)

    assert repository.get(*_key(established)) == ended


def test_ended_relationship_remains_present_and_key_reserved() -> None:
    repository = InMemoryRelationshipRepository()
    established = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SIBLING_OF,
    )
    ended = established.end()

    repository.save(established)
    repository.save(ended)

    replacement = Relationship.establish(
        established.family_id,
        established.source_person_id,
        established.target_person_id,
        established.relationship_type,
    )

    with pytest.raises(RelationshipConflictError):
        repository.save(replacement)

    assert repository.get(*_key(established)) == ended


def test_child_of_and_parent_of_collide_after_domain_normalization() -> None:
    repository = InMemoryRelationshipRepository()
    parent_view = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    child_view = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.CHILD_OF,
    )

    assert _key(parent_view) == _key(child_view)

    repository.save(parent_view)

    with pytest.raises(RelationshipConflictError):
        repository.save(child_view)

    assert repository.get(*_key(parent_view)) is parent_view


@pytest.mark.parametrize(
    "relationship_type",
    [RelationshipType.SPOUSE_OF, RelationshipType.SIBLING_OF],
)
def test_reversed_symmetric_views_collide_after_domain_normalization(
    relationship_type: RelationshipType,
) -> None:
    repository = InMemoryRelationshipRepository()
    forward = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        relationship_type,
    )
    reversed_view = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        relationship_type,
    )

    assert _key(forward) == _key(reversed_view)

    repository.save(forward)

    with pytest.raises(RelationshipConflictError):
        repository.save(reversed_view)

    assert repository.get(*_key(forward)) is forward


def test_same_relationship_fact_in_another_family_is_distinct() -> None:
    repository = InMemoryRelationshipRepository()
    first = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    second = Relationship.establish(
        FamilyId(UUID("87654321-4321-4321-8321-cba987654321")),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )

    repository.save(first)
    repository.save(second)

    assert repository.get(*_key(first)) is first
    assert repository.get(*_key(second)) is second


@pytest.mark.parametrize(
    ("existing_state", "candidate_state"),
    [
        (RelationshipState.ESTABLISHED, RelationshipState.ESTABLISHED),
        (RelationshipState.ENDED, RelationshipState.ESTABLISHED),
        (RelationshipState.ENDED, RelationshipState.ENDED),
    ],
)
def test_save_rejects_noncanonical_replacement(
    existing_state: RelationshipState,
    candidate_state: RelationshipState,
) -> None:
    repository = InMemoryRelationshipRepository()
    established = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    repository.save(established)

    current = established
    if existing_state is RelationshipState.ENDED:
        current = established.end()
        repository.save(current)

    candidate = Relationship(
        family_id=current.family_id,
        source_person_id=current.source_person_id,
        target_person_id=current.target_person_id,
        relationship_type=current.relationship_type,
        state=candidate_state,
    )

    with pytest.raises(
        RelationshipConflictError,
        match="Relationship persistence must preserve one canonical continuity",
    ):
        repository.save(candidate)

    assert repository.get(*_key(current)) == current


def test_get_does_not_apply_competing_child_of_normalization() -> None:
    repository = InMemoryRelationshipRepository()
    canonical = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    repository.save(canonical)

    assert repository.get(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.CHILD_OF,
    ) is None
    assert repository.get(*_key(canonical)) is canonical


def test_get_does_not_apply_competing_symmetric_normalization() -> None:
    repository = InMemoryRelationshipRepository()
    canonical = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    repository.save(canonical)

    assert repository.get(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.SPOUSE_OF,
    ) is None
    assert repository.get(*_key(canonical)) is canonical


def test_concurrent_initial_save_establishes_canonical_key_exactly_once() -> None:
    relationships = tuple(
        Relationship.establish(
            _family_id(),
            _low_person_id(),
            _high_person_id(),
            RelationshipType.SIBLING_OF,
        )
        for _ in range(8)
    )
    barrier = Barrier(len(relationships))
    repository = InMemoryRelationshipRepository()

    def attempt_save(relationship: Relationship) -> bool:
        barrier.wait()

        try:
            repository.save(relationship)
        except RelationshipConflictError:
            return False

        return True

    with ThreadPoolExecutor(max_workers=len(relationships)) as executor:
        outcomes = tuple(executor.map(attempt_save, relationships))

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(relationships) - 1

    stored = repository.get(*_key(relationships[0]))
    assert stored is relationships[outcomes.index(True)]
