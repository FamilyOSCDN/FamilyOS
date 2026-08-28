"""Canonical Family Membership entity."""

from __future__ import annotations

from dataclasses import dataclass, replace

from familyos_cli.domain.family.family_id import FamilyId
from familyos_cli.domain.family.membership_state import MembershipState
from familyos_cli.domain.person import PersonId


class InvalidMembershipTransitionError(Exception):
    """Raised when a Membership lifecycle transition is not canonical."""


@dataclass(frozen=True, slots=True)
class Membership:
    """Canonical Membership identified by the (FamilyId, PersonId) business key."""

    family_id: FamilyId
    person_id: PersonId
    state: MembershipState

    def __post_init__(self) -> None:
        """Require canonical Family, Person, and lifecycle values."""
        if not isinstance(self.family_id, FamilyId):
            raise TypeError("Membership family_id must be a FamilyId")

        if not isinstance(self.person_id, PersonId):
            raise TypeError("Membership person_id must be a PersonId")

        if not isinstance(self.state, MembershipState):
            raise TypeError("Membership state must be a MembershipState")

    @classmethod
    def establish(cls, family_id: FamilyId, person_id: PersonId) -> Membership:
        """Establish one new canonical Membership in PENDING state."""
        return cls(
            family_id=family_id,
            person_id=person_id,
            state=MembershipState.PENDING,
        )

    @property
    def is_currently_valid(self) -> bool:
        """Return whether the Membership is valid for current participation."""
        return self.state is MembershipState.ACTIVE

    def activate(self) -> Membership:
        """Activate a PENDING or SUSPENDED Membership continuity."""
        if self.state not in {MembershipState.PENDING, MembershipState.SUSPENDED}:
            self._raise_invalid_transition(MembershipState.ACTIVE)

        return replace(self, state=MembershipState.ACTIVE)

    def suspend(self) -> Membership:
        """Suspend an ACTIVE Membership continuity."""
        if self.state is not MembershipState.ACTIVE:
            self._raise_invalid_transition(MembershipState.SUSPENDED)

        return replace(self, state=MembershipState.SUSPENDED)

    def end(self) -> Membership:
        """End a non-terminal Membership continuity."""
        if self.state not in {
            MembershipState.PENDING,
            MembershipState.ACTIVE,
            MembershipState.SUSPENDED,
        }:
            self._raise_invalid_transition(MembershipState.ENDED)

        return replace(self, state=MembershipState.ENDED)

    def _raise_invalid_transition(self, target: MembershipState) -> None:
        raise InvalidMembershipTransitionError(
            f"Membership transition {self.state.value} -> {target.value} is not allowed"
        )
