"""Generic plugin contribution registry."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from typing import TypeVar, cast

from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)

ContributionType = TypeVar(
    "ContributionType",
    bound=Contribution,
)


class ContributionRegistry:
    """Store and resolve plugin contributions by concrete type."""

    def __init__(self) -> None:
        """Initialize an empty contribution registry."""

        self._contributions: dict[
            type[Contribution],
            list[Contribution],
        ] = defaultdict(list)

    def register(
        self,
        contribution: Contribution,
    ) -> None:
        """Register a contribution by its concrete type."""

        contribution_type = type(contribution)

        if contribution in self._contributions[contribution_type]:
            raise ValueError(
                (
                    "Contribution already registered: "
                    f"{contribution!r}"
                ),
            )

        self._contributions[contribution_type].append(
            contribution,
        )

    def unregister(
        self,
        contribution: Contribution,
    ) -> None:
        """Remove a registered contribution."""

        contribution_type = type(contribution)
        contributions = self._contributions.get(
            contribution_type,
        )

        if contributions is None:
            return

        if contribution in contributions:
            contributions.remove(contribution)

        if not contributions:
            self._contributions.pop(
                contribution_type,
                None,
            )

    def get_all(
        self,
        contribution_type: type[ContributionType],
    ) -> tuple[ContributionType, ...]:
        """Return contributions matching a concrete type."""

        contributions = self._contributions.get(
            contribution_type,
            [],
        )

        return cast(
            tuple[ContributionType, ...],
            tuple(contributions),
        )

    def all(
        self,
    ) -> tuple[Contribution, ...]:
        """Return every registered contribution."""

        return tuple(
            contribution
            for contributions in self._contributions.values()
            for contribution in contributions
        )

    def types(
        self,
    ) -> tuple[type[Contribution], ...]:
        """Return registered contribution types."""

        return tuple(
            self._contributions,
        )

    def __iter__(
        self,
    ) -> Iterator[Contribution]:
        """Iterate over registered contributions."""

        return iter(
            self.all(),
        )

    def __len__(
        self,
    ) -> int:
        """Return the number of registered contributions."""

        return sum(
            len(contributions)
            for contributions in self._contributions.values()
        )
