"""Application service for generating canonical build identities."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID, uuid4

from familyos_cli.application.build.build_id import BuildId


@dataclass(frozen=True, slots=True)
class BuildIdGenerator:
    """Generate provider-neutral identities for canonical build executions."""

    uuid_factory: Callable[[], UUID] = uuid4

    def generate(self) -> BuildId:
        """Return a new opaque build identity."""

        return BuildId(self.uuid_factory())
