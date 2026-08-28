"""In-memory adapter for the canonical Membership repository port."""

from threading import Lock

from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.domain.family import FamilyId, Membership, MembershipState
from familyos_cli.domain.person import PersonId

MembershipKey = tuple[FamilyId, PersonId]


class InMemoryMembershipRepository(MembershipRepository):
    """Store canonical Membership continuities by composite business key."""

    def __init__(self) -> None:
        self._memberships: dict[MembershipKey, Membership] = {}
        self._lock = Lock()

    def save(self, membership: Membership) -> None:
        """Persist initial PENDING creation or a canonical lifecycle successor."""

        key = (membership.family_id, membership.person_id)

        with self._lock:
            existing = self._memberships.get(key)

            if existing is None:
                if membership.state is not MembershipState.PENDING:
                    raise MembershipConflictError(
                        "Initial Membership persistence requires PENDING state"
                    )

                self._memberships[key] = membership
                return

            if not self._is_valid_successor(existing, membership):
                raise MembershipConflictError(
                    "Membership persistence must preserve one canonical continuity"
                )

            self._memberships[key] = membership

    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        """Return Membership for the composite key, including ENDED, or absence."""

        with self._lock:
            return self._memberships.get((family_id, person_id))

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
