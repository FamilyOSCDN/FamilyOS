"""Tests for atomic in-memory Relationship temporal persistence."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    RelationshipConflictError,
    RelationshipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEnded,
    FamilyRelationshipEstablished,
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


def _time(minute: int = 0) -> datetime:
    return datetime(2026, 8, 28, 14, minute, tzinfo=UTC)


def _established(
    relationship: Relationship,
    minute: int = 0,
) -> FamilyRelationshipEstablished:
    return FamilyRelationshipEstablished(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
        _time(minute),
    )


def _ended(
    relationship: Relationship,
    minute: int = 1,
) -> FamilyRelationshipEnded:
    return FamilyRelationshipEnded(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
        _time(minute),
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

    repository.save(relationship, _established(relationship))

    assert repository.get(*_key(relationship)) == relationship


def test_get_returns_none_for_absent_canonical_key() -> None:
    repository = InMemoryRelationshipRepository()

    assert (
        repository.get(
            _family_id(),
            _low_person_id(),
            _high_person_id(),
            RelationshipType.PARENT_OF,
        )
        is None
    )


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
        repository.save(ended, _established(ended))

    assert repository.get(*_key(ended)) is None
    assert _key(ended) not in repository._temporal_facts


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

    repository.save(first, _established(first))

    with pytest.raises(RelationshipConflictError):
        repository.save(second, _established(second, 1))

    assert repository.get(*_key(first)) is first
    assert repository._temporal_facts[_key(first)] == (_established(first),)


def test_save_accepts_only_established_to_ended_successor() -> None:
    established = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    ended = established.end()
    repository = InMemoryRelationshipRepository()

    repository.save(established, _established(established))
    end_event = _ended(ended)
    repository.save(ended, end_event)

    assert repository.get(*_key(established)) == ended
    assert repository._temporal_facts[_key(established)][-1] == end_event


def test_ended_relationship_remains_present_and_key_reserved() -> None:
    repository = InMemoryRelationshipRepository()
    established = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SIBLING_OF,
    )
    ended = established.end()

    repository.save(established, _established(established))
    end_event = _ended(ended)
    repository.save(ended, end_event)

    replacement = Relationship.establish(
        established.family_id,
        established.source_person_id,
        established.target_person_id,
        established.relationship_type,
    )

    with pytest.raises(RelationshipConflictError):
        repository.save(replacement, _established(replacement, 2))

    assert repository.get(*_key(established)) == ended
    assert repository._temporal_facts[_key(established)] == (
        _established(established),
        end_event,
    )


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

    repository.save(parent_view, _established(parent_view))

    with pytest.raises(RelationshipConflictError):
        repository.save(child_view, _established(child_view, 1))

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

    repository.save(forward, _established(forward))

    with pytest.raises(RelationshipConflictError):
        repository.save(reversed_view, _established(reversed_view, 1))

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

    repository.save(first, _established(first))
    repository.save(second, _established(second, 1))

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
    repository.save(established, _established(established))

    current = established
    if existing_state is RelationshipState.ENDED:
        current = established.end()
        repository.save(current, _ended(current))

    before_facts = repository._temporal_facts[_key(current)]
    candidate = Relationship(
        family_id=current.family_id,
        source_person_id=current.source_person_id,
        target_person_id=current.target_person_id,
        relationship_type=current.relationship_type,
        state=candidate_state,
    )

    with pytest.raises(RelationshipConflictError):
        repository.save(candidate, _established(candidate, 10))

    assert repository.get(*_key(current)) == current
    assert repository._temporal_facts[_key(current)] == before_facts


def test_get_does_not_apply_competing_child_of_normalization() -> None:
    repository = InMemoryRelationshipRepository()
    canonical = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    repository.save(canonical, _established(canonical))

    assert (
        repository.get(
            _family_id(),
            _high_person_id(),
            _low_person_id(),
            RelationshipType.CHILD_OF,
        )
        is None
    )
    assert repository.get(*_key(canonical)) is canonical


def test_get_does_not_apply_competing_symmetric_normalization() -> None:
    repository = InMemoryRelationshipRepository()
    canonical = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    repository.save(canonical, _established(canonical))

    assert (
        repository.get(
            _family_id(),
            _high_person_id(),
            _low_person_id(),
            RelationshipType.SPOUSE_OF,
        )
        is None
    )
    assert repository.get(*_key(canonical)) is canonical


def test_establish_and_end_preserve_both_temporal_facts() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    ended = relationship.end()
    repository = InMemoryRelationshipRepository()
    established_event = _established(relationship)
    ended_event = FamilyRelationshipEnded(
        ended.family_id,
        ended.source_person_id,
        ended.target_person_id,
        ended.relationship_type,
        established_event.occurred_at + timedelta(minutes=1),
    )

    repository.save(relationship, established_event)
    repository.save(ended, ended_event)

    assert repository.get(*_key(relationship)) == ended
    assert repository._temporal_facts[_key(relationship)] == (
        established_event,
        ended_event,
    )


def test_wrong_transition_fact_is_atomic_conflict() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    repository = InMemoryRelationshipRepository()
    established_event = _established(relationship)
    repository.save(relationship, established_event)
    ended = relationship.end()
    wrong = _established(ended, 1)

    with pytest.raises(
        RelationshipConflictError,
        match="temporal fact must match canonical lifecycle transition",
    ):
        repository.save(ended, wrong)

    assert repository.get(*_key(relationship)) == relationship
    assert repository._temporal_facts[_key(relationship)] == (established_event,)


def test_temporal_fact_identity_mismatch_is_atomic_conflict() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SIBLING_OF,
    )
    repository = InMemoryRelationshipRepository()
    wrong = FamilyRelationshipEstablished(
        relationship.family_id,
        relationship.target_person_id,
        relationship.source_person_id,
        relationship.relationship_type,
        _time(),
    )

    with pytest.raises(RelationshipConflictError, match="must match canonical"):
        repository.save(relationship, wrong)

    assert repository.get(*_key(relationship)) is None
    assert _key(relationship) not in repository._temporal_facts


def test_initial_ended_state_is_rejected_without_temporal_persistence() -> None:
    ended = Relationship(
        family_id=_family_id(),
        source_person_id=_low_person_id(),
        target_person_id=_high_person_id(),
        relationship_type=RelationshipType.PARENT_OF,
        state=RelationshipState.ENDED,
    )
    repository = InMemoryRelationshipRepository()

    with pytest.raises(RelationshipConflictError):
        repository.save(ended, _established(ended))

    assert repository.get(*_key(ended)) is None
    assert _key(ended) not in repository._temporal_facts


def test_ended_relationship_reserves_key_and_preserves_facts() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    ended = relationship.end()
    repository = InMemoryRelationshipRepository()
    established_event = _established(relationship)
    ended_event = _ended(ended)

    repository.save(relationship, established_event)
    repository.save(ended, ended_event)

    replacement = Relationship.establish(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
    )
    with pytest.raises(RelationshipConflictError):
        repository.save(replacement, _established(replacement, 2))

    assert repository.get(*_key(relationship)) == ended
    assert repository._temporal_facts[_key(relationship)] == (
        established_event,
        ended_event,
    )


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
    events = tuple(
        _established(relationship, index)
        for index, relationship in enumerate(relationships)
    )
    barrier = Barrier(len(relationships))
    repository = InMemoryRelationshipRepository()

    def attempt_save(
        item: tuple[Relationship, FamilyRelationshipEstablished],
    ) -> bool:
        relationship, event = item
        barrier.wait()
        try:
            repository.save(relationship, event)
        except RelationshipConflictError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=len(relationships)) as executor:
        outcomes = tuple(
            executor.map(
                attempt_save,
                zip(relationships, events, strict=True),
            )
        )

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(relationships) - 1
    winner = outcomes.index(True)
    key = _key(relationships[winner])
    assert repository.get(*key) is relationships[winner]
    assert repository._temporal_facts[key] == (events[winner],)


def test_concurrent_initial_save_establishes_key_and_fact_exactly_once() -> None:
    # Explicit F4.11 atomicity assertion retained alongside the historical name.
    test_concurrent_initial_save_establishes_canonical_key_exactly_once()
