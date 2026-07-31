"""Tests for plugin resolution diagnostic reports."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticReport,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)


def make_diagnostic(
    severity: DiagnosticSeverity,
) -> PluginResolutionDiagnostic:
    """Create a diagnostic for report tests."""

    return PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=severity,
        message=f"{severity.value} diagnostic",
    )


def test_diagnostic_report_is_empty_by_default() -> None:
    """A new report contains no diagnostics and is successful."""

    report = DiagnosticReport()

    assert report.diagnostics == ()
    assert report.is_empty()
    assert report.is_success()
    assert not report.has_errors()


def test_diagnostic_report_add_returns_new_report() -> None:
    """Adding a diagnostic preserves report immutability."""

    diagnostic = make_diagnostic(DiagnosticSeverity.ERROR)
    report = DiagnosticReport()

    updated_report = report.add(diagnostic)

    assert report.diagnostics == ()
    assert updated_report.diagnostics == (diagnostic,)


def test_diagnostic_report_extend_returns_new_report() -> None:
    """Extending a report appends diagnostics in order."""

    info = make_diagnostic(DiagnosticSeverity.INFO)
    warning = make_diagnostic(DiagnosticSeverity.WARNING)
    error = make_diagnostic(DiagnosticSeverity.ERROR)

    report = DiagnosticReport((info,))
    updated_report = report.extend((warning, error))

    assert report.diagnostics == (info,)
    assert updated_report.diagnostics == (
        info,
        warning,
        error,
    )


def test_diagnostic_report_filters_by_severity() -> None:
    """A report returns diagnostics grouped by severity."""

    info = make_diagnostic(DiagnosticSeverity.INFO)
    warning = make_diagnostic(DiagnosticSeverity.WARNING)
    error = make_diagnostic(DiagnosticSeverity.ERROR)

    report = DiagnosticReport(
        diagnostics=(
            info,
            warning,
            error,
        ),
    )

    assert report.infos() == (info,)
    assert report.warnings() == (warning,)
    assert report.errors() == (error,)


def test_diagnostic_report_detects_errors() -> None:
    """A report containing an error is not successful."""

    report = DiagnosticReport().add(
        make_diagnostic(DiagnosticSeverity.ERROR),
    )

    assert report.has_errors()
    assert not report.is_success()
    assert not report.is_empty()


def test_diagnostic_report_with_warnings_remains_successful() -> None:
    """Warnings do not cause resolution failure."""

    report = DiagnosticReport().add(
        make_diagnostic(DiagnosticSeverity.WARNING),
    )

    assert not report.has_errors()
    assert report.is_success()
