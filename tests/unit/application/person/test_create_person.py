"""Tests for canonical CreatePerson application semantics."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from familyos_cli.application.person import CreatePerson
from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonId


class RecordingPersonRepository(PersonRepository):
    """Minimal repository test double recording canonical saves."""

    def __init__(self) -> None:
        self.saved: list[Person] = []

    def save(self, person: Person) -> None:
        self.saved.append(person)

    def get(self, person_id: PersonId) -> Person | None:
        return next(
            (person for person in self.saved if person.person_id == person_id),
            None,
        )


def test_create_person_persists_exactly_one_person_and_returns_event() -> None:
    """Successful creation persists one Person and returns its creation fact."""

    repository = RecordingPersonRepository()
    person_id = PersonId(UUID("12345678-1234-4234-8234-123456789abc"))
    occurred_at = datetime(2026, 8, 27, 12, 0, tzinfo=UTC)

    use_case = CreatePerson(
        repository,
        person_id_factory=lambda: person_id,
        clock=lambda: occurred_at,
    )

    result = use_case.execute()

    assert repository.saved == [result.person]
    assert result.person.person_id == person_id
    assert result.event.person_id == person_id
    assert result.event.occurred_at == occurred_at


def test_create_person_uses_injected_identity_factory_once() -> None:
    """Canonical identity generation is controlled by the application boundary."""

    repository = RecordingPersonRepository()
    person_id = PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    calls = 0

    def generate_person_id() -> PersonId:
        nonlocal calls
        calls += 1
        return person_id

    use_case = CreatePerson(
        repository,
        person_id_factory=generate_person_id,
        clock=lambda: datetime(2026, 8, 27, 12, 0, tzinfo=UTC),
    )

    result = use_case.execute()

    assert calls == 1
    assert result.person.person_id == person_id


def test_create_person_uses_injected_clock_once() -> None:
    """PersonCreated occurrence time comes from the application clock boundary."""

    repository = RecordingPersonRepository()
    occurred_at = datetime(2026, 8, 27, 13, 30, tzinfo=UTC)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return occurred_at

    use_case = CreatePerson(repository, clock=clock)

    result = use_case.execute()

    assert calls == 1
    assert result.event.occurred_at == occurred_at


def test_create_person_propagates_identity_factory_failure() -> None:
    """Identity-generation failure remains distinct and propagates unchanged."""

    repository = RecordingPersonRepository()

    def failing_person_id_factory() -> PersonId:
        raise RuntimeError("identity generation unavailable")

    use_case = CreatePerson(
        repository,
        person_id_factory=failing_person_id_factory,
        clock=lambda: datetime(2026, 8, 27, 17, 0, tzinfo=UTC),
    )

    with pytest.raises(
        RuntimeError,
        match="identity generation unavailable",
    ):
        use_case.execute()

    assert repository.saved == []


def test_create_person_propagates_repository_failure() -> None:
    """Persistence failure is not translated into successful Person creation."""

    class FailingRepository(PersonRepository):
        def save(self, person: Person) -> None:
            raise RuntimeError("persistence unavailable")

        def get(self, person_id: PersonId) -> Person | None:
            return None

    person_id = PersonId(UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd"))

    use_case = CreatePerson(
        FailingRepository(),
        person_id_factory=lambda: person_id,
        clock=lambda: datetime(2026, 8, 27, 17, 30, tzinfo=UTC),
    )

    with pytest.raises(
        RuntimeError,
        match="persistence unavailable",
    ):
        use_case.execute()


def test_create_person_propagates_clock_failure_before_persistence() -> None:
    """Clock failure propagates before canonical Person persistence."""

    repository = RecordingPersonRepository()
    person_id = PersonId(UUID("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"))

    def failing_clock() -> datetime:
        raise RuntimeError("clock unavailable")

    use_case = CreatePerson(
        repository,
        person_id_factory=lambda: person_id,
        clock=failing_clock,
    )

    with pytest.raises(
        RuntimeError,
        match="clock unavailable",
    ):
        use_case.execute()

    assert repository.saved == []


def test_create_person_rejects_naive_occurrence_time_before_persistence() -> None:
    """Invalid PersonCreated time fails before the Person is persisted."""

    repository = RecordingPersonRepository()
    person_id = PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))

    use_case = CreatePerson(
        repository,
        person_id_factory=lambda: person_id,
        clock=lambda: datetime(2026, 8, 27, 18, 0),
    )

    with pytest.raises(
        ValueError,
        match="PersonCreated occurrence time must be timezone-aware",
    ):
        use_case.execute()

    assert repository.saved == []
