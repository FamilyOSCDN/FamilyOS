"""Plugin version value object."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering

_VERSION_PATTERN = re.compile(
    r"^(?P<major>0|[1-9]\d*)"
    r"\.(?P<minor>0|[1-9]\d*)"
    r"\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<pre_release>"
    r"(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*"
    r"))?"
    r"(?:\+(?P<build_metadata>"
    r"[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*"
    r"))?$",
)


@total_ordering
@dataclass(frozen=True, slots=True)
class PluginVersion:
    """Represent a comparable semantic plugin version."""

    major: int
    minor: int
    patch: int
    pre_release: tuple[str, ...] = ()
    build_metadata: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate version components."""

        if self.major < 0:
            raise ValueError(
                "Plugin version major component must be non-negative.",
            )

        if self.minor < 0:
            raise ValueError(
                "Plugin version minor component must be non-negative.",
            )

        if self.patch < 0:
            raise ValueError(
                "Plugin version patch component must be non-negative.",
            )

        for identifier in self.pre_release:
            if not identifier:
                raise ValueError(
                    "Pre-release identifiers must not be empty.",
                )

            if identifier.isdigit() and (
                len(identifier) > 1
                and identifier.startswith("0")
            ):
                raise ValueError(
                    "Numeric pre-release identifiers must not "
                    "contain leading zeroes.",
                )

        for identifier in self.build_metadata:
            if not identifier:
                raise ValueError(
                    "Build metadata identifiers must not be empty.",
                )

    @classmethod
    def parse(
        cls,
        value: str,
    ) -> PluginVersion:
        """Parse a semantic plugin version string.

        Args:
            value: Semantic version string.

        Returns:
            Parsed plugin version.

        Raises:
            ValueError: If the version is invalid.
        """

        match = _VERSION_PATTERN.fullmatch(
            value,
        )

        if match is None:
            raise ValueError(
                f"Invalid plugin version: {value!r}.",
            )

        pre_release_value = match.group(
            "pre_release",
        )
        build_metadata_value = match.group(
            "build_metadata",
        )

        return cls(
            major=int(
                match.group("major"),
            ),
            minor=int(
                match.group("minor"),
            ),
            patch=int(
                match.group("patch"),
            ),
            pre_release=(
                tuple(pre_release_value.split("."))
                if pre_release_value
                else ()
            ),
            build_metadata=(
                tuple(build_metadata_value.split("."))
                if build_metadata_value
                else ()
            ),
        )

    @property
    def is_pre_release(
        self,
    ) -> bool:
        """Return whether this version is a pre-release."""

        return bool(self.pre_release)

    def __str__(self) -> str:
        """Return the canonical semantic version string."""

        value = (
            f"{self.major}."
            f"{self.minor}."
            f"{self.patch}"
        )

        if self.pre_release:
            value += (
                "-"
                + ".".join(self.pre_release)
            )

        if self.build_metadata:
            value += (
                "+"
                + ".".join(self.build_metadata)
            )

        return value

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """Return whether two versions have equal precedence."""

        if not isinstance(other, PluginVersion):
            return NotImplemented

        return (
            self.major,
            self.minor,
            self.patch,
            self.pre_release,
        ) == (
            other.major,
            other.minor,
            other.patch,
            other.pre_release,
        )

    def __lt__(
        self,
        other: object,
    ) -> bool:
        """Return whether this version has lower precedence."""

        if not isinstance(other, PluginVersion):
            return NotImplemented

        current_core = (
            self.major,
            self.minor,
            self.patch,
        )
        other_core = (
            other.major,
            other.minor,
            other.patch,
        )

        if current_core != other_core:
            return current_core < other_core

        return self._compare_pre_release(
            self.pre_release,
            other.pre_release,
        ) < 0

    @staticmethod
    def _compare_pre_release(
        current: tuple[str, ...],
        other: tuple[str, ...],
    ) -> int:
        """Compare semantic version pre-release identifiers."""

        if not current and not other:
            return 0

        if not current:
            return 1

        if not other:
            return -1

        for current_identifier, other_identifier in zip(
            current,
            other,
            strict=False,
        ):
            if current_identifier == other_identifier:
                continue

            current_numeric = (
                current_identifier.isdigit()
            )
            other_numeric = (
                other_identifier.isdigit()
            )

            if current_numeric and other_numeric:
                return (
                    -1
                    if int(current_identifier)
                    < int(other_identifier)
                    else 1
                )

            if current_numeric:
                return -1

            if other_numeric:
                return 1

            return (
                -1
                if current_identifier < other_identifier
                else 1
            )

        if len(current) == len(other):
            return 0

        return -1 if len(current) < len(other) else 1
