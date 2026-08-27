"""Integration tests for canonical Person create/retrieve flow."""

from datetime import UTC, datetime
from uuid import UUID

from familyos_cli.application.person import CreatePerson, GetPerson
from familyos_cli.domain.person import PersonId
from familyos_cli.infrastructure.person import InMemoryPersonRepository


def test_create_then_get_returns_same_canonical_person() -> None:
    """CreatePerson and GetPerson compose through the canonical repository port."""

    repository = InMemoryPersonRepository()
    person_id = PersonId(UUID("12345678-1234-4234-8234-123456789abc"))
    occurred_at = datetime(2026, 8, 27, 14, 0, tzinfo=UTC)

    create_person = CreatePerson(
        repository,
        person_id_factory=lambda: person_id,
        clock=lambda: occurred_at,
    )
    get_person = GetPerson(repository)

    creation = create_person.execute()
    retrieved = get_person.execute(person_id)

    assert retrieved == creation.person
    assert creation.person.person_id == person_id
    assert creation.event.person_id == person_id
    assert creation.event.occurred_at == occurred_at


def test_get_before_create_returns_none_then_returns_person_after_create() -> None:
    """Canonical absence transitions to presence only after successful creation."""

    repository = InMemoryPersonRepository()
    person_id = PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))

    get_person = GetPerson(repository)

    assert get_person.execute(person_id) is None

    CreatePerson(
        repository,
        person_id_factory=lambda: person_id,
        clock=lambda: datetime(2026, 8, 27, 15, 0, tzinfo=UTC),
    ).execute()

    retrieved = get_person.execute(person_id)

    assert retrieved is not None
    assert retrieved.person_id == person_id


def test_two_creations_with_distinct_ids_remain_independently_retrievable() -> None:
    """Distinct canonical Person identities remain independently addressable."""

    repository = InMemoryPersonRepository()
    first_id = PersonId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
    second_id = PersonId(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))

    CreatePerson(
        repository,
        person_id_factory=lambda: first_id,
        clock=lambda: datetime(2026, 8, 27, 16, 0, tzinfo=UTC),
    ).execute()

    CreatePerson(
        repository,
        person_id_factory=lambda: second_id,
        clock=lambda: datetime(2026, 8, 27, 16, 5, tzinfo=UTC),
    ).execute()

    get_person = GetPerson(repository)

    first = get_person.execute(first_id)
    second = get_person.execute(second_id)

    assert first is not None
    assert second is not None
    assert first.person_id == first_id
    assert second.person_id == second_id
    assert first != second
