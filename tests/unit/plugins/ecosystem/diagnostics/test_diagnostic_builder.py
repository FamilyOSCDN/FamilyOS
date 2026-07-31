"""Tests for the plugin resolution diagnostic builder."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticBuilder,
    DiagnosticKind,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)


def make_diagnostic(
    message: str,
) -> PluginResolutionDiagnostic:
    """Create a diagnostic for builder tests."""

    return PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=DiagnosticSeverity.INFO,
        message=message,
    )


def test_diagnostic_builder_is_empty_by_default() -> None:
    """A new builder contains no diagnostics."""

    builder = DiagnosticBuilder()

    assert builder.is_empty()
    assert builder.count() == 0
    assert builder.build().is_empty()


def test_diagnostic_builder_adds_diagnostic() -> None:
    """A builder adds a diagnostic fluently."""

    diagnostic = make_diagnostic("Resolution started.")
    builder = DiagnosticBuilder()

    returned_builder = builder.add(diagnostic)
    report = builder.build()

    assert returned_builder is builder
    assert builder.count() == 1
    assert not builder.is_empty()
    assert report.diagnostics == (diagnostic,)


def test_diagnostic_builder_adds_many_diagnostics() -> None:
    """A builder adds multiple diagnostics in order."""

    first = make_diagnostic("Resolution started.")
    second = make_diagnostic("Resolution completed.")
    builder = DiagnosticBuilder()

    returned_builder = builder.add_many((first, second))
    report = builder.build()

    assert returned_builder is builder
    assert builder.count() == 2
    assert report.diagnostics == (
        first,
        second,
    )


def test_diagnostic_builder_supports_fluent_chaining() -> None:
    """Builder operations can be chained fluently."""

    first = make_diagnostic("First diagnostic.")
    second = make_diagnostic("Second diagnostic.")

    report = (
        DiagnosticBuilder()
        .add(first)
        .add(second)
        .build()
    )

    assert report.diagnostics == (
        first,
        second,
    )


def test_diagnostic_builder_build_returns_immutable_snapshot() -> None:
    """A built report is not modified by later builder changes."""

    first = make_diagnostic("First diagnostic.")
    second = make_diagnostic("Second diagnostic.")
    builder = DiagnosticBuilder().add(first)

    first_report = builder.build()
    builder.add(second)
    second_report = builder.build()

    assert first_report.diagnostics == (first,)
    assert second_report.diagnostics == (
        first,
        second,
    )


def test_diagnostic_builder_clear_removes_diagnostics() -> None:
    """Clearing a builder removes accumulated diagnostics."""

    diagnostic = make_diagnostic("Resolution started.")
    builder = DiagnosticBuilder().add(diagnostic)

    returned_builder = builder.clear()

    assert returned_builder is builder
    assert builder.is_empty()
    assert builder.count() == 0
    assert builder.build().diagnostics == ()
