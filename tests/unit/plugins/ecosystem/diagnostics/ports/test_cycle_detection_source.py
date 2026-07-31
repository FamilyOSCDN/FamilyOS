"""Tests for the cycle detection source protocol."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    CycleDetectionSource,
)


class FakeCycleDetectionSource:
    """Simple graph source implementation."""

    def plugins(self) -> tuple[str, ...]:
        return (
            "security",
            "crypto",
        )

    def dependencies_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        if plugin == "security":
            return ("crypto",)

        return ()


def test_cycle_detection_source_protocol() -> None:
    """A concrete source satisfies the protocol."""

    source: CycleDetectionSource = (
        FakeCycleDetectionSource()
    )

    assert source.plugins() == (
        "security",
        "crypto",
    )
    assert source.dependencies_of(
        "security",
    ) == (
        "crypto",
    )
