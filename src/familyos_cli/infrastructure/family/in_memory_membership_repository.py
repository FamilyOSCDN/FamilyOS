"""In-memory adapter for canonical Membership temporal persistence."""

from threading import Lock

from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
    MembershipTemporalFact,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipCreated,
    FamilyMembershipEnded,
    FamilyMembershipReactivated,
    FamilyMembershipSuspended,
    Membership,
    MembershipState,
)
from familyos_cli.domain.person import PersonId

MembershipKey = tuple[FamilyId, PersonId]


class InMemoryMembershipRepository(MembershipRepository):
    """Atomically store Membership continuity and required temporal facts."""

    def __init__(self) -> None:
        self._memberships: dict[MembershipKey, Membership] = {}
        self._temporal_facts: dict[
            MembershipKey,
            tuple[MembershipTemporalFact, ...],
        ] = {}
        self._lock = Lock()

    def save(
        self,
        membership: Membership,
        temporal_fact: MembershipTemporalFact,
    ) -> None:
        """Persist one canonical transition and its occurrence fact atomically."""

        key = (membership.family_id, membership.person_id)

        with self._lock:
            existing = self._memberships.get(key)
            self._validate_temporal_fact(
                existing=existing,
                candidate=membership,
                temporal_fact=temporal_fact,
            )

            if existing is None:
                if membership.state is not MembershipState.PENDING:
                    raise MembershipConflictError(
                        "Initial Membership persistence requires PENDING state"
                    )
            elif not self._is_valid_successor(existing, membership):
                raise MembershipConflictError(
                    "Membership persistence must preserve one canonical continuity"
                )

            existing_facts = self._temporal_facts.get(key, ())
            self._memberships[key] = membership
            self._temporal_facts[key] = (*existing_facts, temporal_fact)

    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        """Return Membership for the composite key, including ENDED, or absence."""

        with self._lock:
            return self._memberships.get((family_id, person_id))

    @staticmethod
    def _validate_temporal_fact(
        *,
        existing: Membership | None,
        candidate: Membership,
        temporal_fact: MembershipTemporalFact,
    ) -> None:
        if (
            temporal_fact.family_id != candidate.family_id
            or temporal_fact.person_id != candidate.person_id
        ):
            raise MembershipConflictError(
                "Membership temporal fact must match canonical Membership identity"
            )

        if existing is None:
            if not isinstance(temporal_fact, FamilyMembershipCreated):
                raise MembershipConflictError(
                    "Initial Membership persistence requires creation temporal fact"
                )
            return

        expected_type: type[MembershipTemporalFact]
        if (
            existing.state is MembershipState.PENDING
            and candidate.state is MembershipState.ACTIVE
        ):
            expected_type = FamilyMembershipActivated
        elif (
            existing.state is MembershipState.ACTIVE
            and candidate.state is MembershipState.SUSPENDED
        ):
            expected_type = FamilyMembershipSuspended
        elif (
            existing.state is MembershipState.SUSPENDED
            and candidate.state is MembershipState.ACTIVE
        ):
            expected_type = FamilyMembershipReactivated
        elif candidate.state is MembershipState.ENDED and existing.state in {
            MembershipState.PENDING,
            MembershipState.ACTIVE,
            MembershipState.SUSPENDED,
        }:
            expected_type = FamilyMembershipEnded
        else:
            raise MembershipConflictError(
                "Membership persistence must preserve one canonical continuity"
            )

        if not isinstance(temporal_fact, expected_type):
            raise MembershipConflictError(
                "Membership temporal fact must match canonical lifecycle transition"
            )

    @staticmethod
    def _is_valid_successor(existing: Membership, candidate: Membership) -> bool:
        if existing.state is MembershipState.PENDING:
            return candidate.state in {
                MembershipState.ACTIVE,
                MembershipState.ENDED,
            }

        if existing.state is MembershipState.ACTIVE:
            return candidate.state in {
                MembershipState.SUSPENDED,
                MembershipState.ENDED,
            }

        if existing.state is MembershipState.SUSPENDED:
            return candidate.state in {
                MembershipState.ACTIVE,
                MembershipState.ENDED,
            }

        return False
