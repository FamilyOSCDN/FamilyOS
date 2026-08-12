# RFC-0006 — Plugin Resolution Diagnostics

## Status

Accepted

## Title

Plugin Resolution Diagnostics

## Summary

This RFC defines the canonical diagnostic architecture used by the FamilyOS
plugin resolution subsystem.

The architecture separates technical resolver diagnostics from enriched plugin
resolution diagnostics and provides a deterministic pipeline for adapting,
aggregating, explaining, suggesting, formatting, and rendering resolution
problems.

It defines:

- technical resolution diagnostics;
- diagnostic codes and severities;
- enriched plugin resolution diagnostics;
- diagnostic kinds;
- canonical plugin identity inside diagnostics;
- diagnostic reports;
- diagnostic adapters;
- diagnostic pipelines;
- conflict and cycle diagnostics;
- explanations and remediation suggestions;
- diagnostic formatting and CLI rendering.

RFC-0004 governs Plugin Versioning & Compatibility.

RFC-0005 governs Plugin Dependency Graph structure and resolution.

---

## 1. Context

Plugin resolution may fail or produce warnings for multiple reasons.

Examples include:

- missing plugins;
- missing dependencies;
- version conflicts;
- unsatisfiable constraints;
- dependency cycles;
- invalid packages;
- unknown plugins;
- general resolution failures.

Returning only exceptions or unstructured strings is insufficient for a
deterministic plugin ecosystem.

FamilyOS therefore models resolution problems as structured diagnostics.

The diagnostic architecture provides both a technical resolver-level model and
an enriched plugin-facing diagnostic model.

---

## 2. Goals

This RFC defines the canonical architecture for plugin resolution diagnostics.

The architecture SHALL provide:

1. structured technical diagnostics;
2. stable diagnostic codes;
3. stable severity levels;
4. enriched diagnostic kinds;
5. canonical Plugin Identifier handling;
6. deterministic diagnostic adaptation;
7. immutable diagnostic reports;
8. conflict and cycle diagnostics;
9. diagnostic explanation;
10. remediation suggestions;
11. machine-readable and human-readable formatting;
12. CLI rendering support.

---

## 3. Non-Goals

This RFC does not redefine:

- Plugin Identifier syntax;
- plugin dependency graph structure;
- version compatibility rules;
- package selection rules;
- plugin discovery;
- plugin installation;
- runtime lifecycle behavior.

Those concerns are governed by their respective ADRs, specifications, and RFCs.

In particular:

- RFC-0003 governs Plugin Discovery & Distribution;
- RFC-0004 governs Plugin Versioning & Compatibility;
- RFC-0005 governs Plugin Dependency Graph behavior.

---

## 4. Diagnostic Architecture

The FamilyOS diagnostic architecture is layered.

Conceptually:

```text
Plugin Resolver
      │
      ▼
Technical Resolution Diagnostics
      │
      ▼
Diagnostic Adapters
      │
      ▼
Plugin Resolution Diagnostics
      │
      ▼
Diagnostic Report
      │
      ├── Explanation
      ├── Suggestions
      ├── Formatting
      └── CLI Rendering
```

The technical resolver model and the enriched plugin-facing model SHALL remain
conceptually distinct.

---

## 5. Technical Resolution Diagnostic

The low-level resolver diagnostic model is:

```text
ResolutionDiagnostic
```

It represents a diagnostic produced directly during plugin resolution.

The canonical model contains:

```text
ResolutionDiagnostic
    ├── message
    ├── plugin
    ├── code
    └── severity
```

The implementation currently maps these fields to:

```text
message: str
plugin: str | None
code: ResolutionDiagnosticCode
severity: ResolutionDiagnosticSeverity
```

---

## 6. Technical Diagnostic Codes

Technical resolution diagnostics SHALL use explicit diagnostic codes.

The current canonical code set includes:

```text
unspecified
cycle_detected
missing_plugin
missing_dependency
version_conflict
unsatisfiable_constraint
warning
info
```

These values are represented by:

```text
ResolutionDiagnosticCode
```

Diagnostic codes SHALL be machine-readable and stable enough for deterministic
handling.

---

## 7. Technical Diagnostic Severity

Technical resolver diagnostics SHALL use explicit severity.

The canonical severity set is:

```text
info
warning
error
```

These values are represented by:

```text
ResolutionDiagnosticSeverity
```

A technical diagnostic SHALL expose whether it represents an error.

The current implementation provides:

```text
ResolutionDiagnostic.is_error
```

---

## 8. Canonical Plugin Identity

When a technical diagnostic identifies a plugin, that identity SHALL be
normalized through the canonical Plugin Identifier model.

Conceptually:

```text
diagnostic.plugin
        │
        ▼
PluginId
        │
        ▼
canonical Plugin Identifier
```

A diagnostic SHALL NOT establish a separate plugin identity namespace.

If no specific plugin is associated with a diagnostic, the technical model MAY
use a null plugin reference.

---

## 9. Enriched Plugin Resolution Diagnostic

The plugin-facing diagnostic model is:

```text
PluginResolutionDiagnostic
```

It represents an enriched issue or informational result produced during plugin
resolution.

The canonical model contains:

```text
PluginResolutionDiagnostic
    ├── kind
    ├── severity
    ├── message
    ├── plugin
    ├── details
    └── path
```

This model supports richer diagnostic interpretation than the low-level
technical resolver diagnostic.

---

## 10. Diagnostic Kind

Enriched diagnostics SHALL classify their semantic nature using:

```text
DiagnosticKind
```

The current canonical kinds include:

```text
version_conflict
dependency_cycle
missing_dependency
unknown_plugin
invalid_package
resolution_failure
information
```

Diagnostic kinds describe semantic meaning.

They SHALL NOT be confused with presentation text.

---

## 11. Diagnostic Severity

Enriched diagnostics SHALL use:

```text
DiagnosticSeverity
```

The canonical values are:

```text
info
warning
error
```

The enriched diagnostic model SHALL provide explicit predicates for severity.

The current implementation exposes:

```text
is_error()
is_warning()
is_info()
```

---

## 12. Diagnostic Plugin Identity

`PluginResolutionDiagnostic.plugin` SHALL use the canonical Plugin Identifier
when present.

The implementation SHALL normalize plugin identity through:

```text
PluginId
```

The model MAY use an empty plugin value when the diagnostic is not associated
with one specific plugin.

Diagnostic consumers SHALL NOT interpret display names as logical plugin
identity.

---

## 13. Diagnostic Path

A diagnostic MAY include a plugin path.

The canonical field is:

```text
path
```

Each element of a diagnostic path SHALL be normalized as a canonical Plugin
Identifier.

A path MAY represent:

- dependency relationships;
- cycle paths;
- resolution traces;
- other ordered plugin relationships relevant to diagnosis.

Example:

```text
familyos.education
familyos.security
familyos.health
familyos.education
```

A dependency-cycle diagnostic MAY preserve the complete closed cycle path.

---

## 14. Diagnostic Details

A diagnostic MAY contain structured textual details.

The canonical field is:

```text
details
```

Details MAY contain:

- conflicting constraints;
- unavailable versions;
- package problems;
- causal information;
- contextual resolver information.

Details SHALL supplement the diagnostic kind and message.

They SHALL NOT replace stable machine-readable classification.

---

## 15. Diagnostic Report

Multiple enriched diagnostics SHALL be aggregated using:

```text
DiagnosticReport
```

A diagnostic report is immutable.

The canonical model contains:

```text
DiagnosticReport
    └── diagnostics
```

Reports SHALL support adding and extending diagnostics by returning a new
report rather than mutating the existing report.

---

## 16. Diagnostic Report Queries

A diagnostic report SHALL support deterministic severity-based queries.

The current implementation provides:

```text
errors()
warnings()
infos()
has_errors()
is_success()
is_empty()
```

`is_success()` SHALL mean that the report contains no error diagnostics.

Warnings and informational diagnostics SHALL NOT by themselves make a report
unsuccessful.

---

## 17. Diagnostic Adapters

Diagnostic adapters SHALL translate lower-level resolution information into
canonical enriched diagnostics.

Examples include:

```text
ConflictDiagnosticAdapter
CycleDiagnosticAdapter
ResolutionConflictAdapter
ResolutionConflictDiagnosticAdapter
ResolutionCycleDiagnosticAdapter
```

Adapters form explicit translation boundaries between:

- technical resolver diagnostics;
- conflict models;
- dependency cycles;
- enriched plugin resolution diagnostics.

Adapters SHALL preserve canonical plugin identity.

---

## 18. Conflict Diagnostics

Plugin resolution conflicts MAY originate from:

- missing dependencies;
- incompatible versions;
- invalid packages;
- unresolved resolver diagnostics.

Conflict adapters SHALL convert technical conflict information into appropriate
diagnostic kinds.

Typical mappings include:

```text
missing dependency
    → missing_dependency

invalid package
    → invalid_package

version incompatibility
    → version_conflict
```

The exact implementation mapping MAY evolve.

The semantic distinction SHALL remain stable.

---

## 19. Dependency Cycle Diagnostics

Dependency cycle detection is structurally governed by RFC-0005.

When a cycle is detected, the diagnostic subsystem SHALL be able to convert the
cycle into an enriched diagnostic.

The canonical kind is:

```text
dependency_cycle
```

A cycle diagnostic SHOULD preserve the relevant plugin path.

Example:

```text
familyos.a
→ familyos.b
→ familyos.c
→ familyos.a
```

Cycle diagnostics SHALL be represented structurally rather than only through an
exception message.

---

## 20. Diagnostic Pipeline

The canonical diagnostic pipeline is represented by:

```text
DiagnosticPipeline
```

The current pipeline consumes:

```text
ResolutionPlan
```

and produces:

```text
DiagnosticReport
```

Conceptually:

```text
ResolutionPlan
      │
      ▼
DiagnosticPipeline
      │
      ├── Adapter
      ├── Adapter
      └── Adapter
      │
      ▼
DiagnosticBuilder
      │
      ▼
DiagnosticReport
```

The pipeline SHALL support multiple diagnostic adapters.

---

## 21. Default Pipeline Behavior

When no explicit adapter set is provided, the diagnostic pipeline MAY define a
default adapter set.

The current implementation uses:

```text
ResolutionConflictDiagnosticAdapter
```

as its default adapter.

Pipeline composition MAY evolve.

The semantic contract SHALL remain that a resolution plan can be transformed
into a deterministic diagnostic report.

---

## 22. Diagnostic Builder

Diagnostic construction SHALL be centralized through a builder abstraction when
multiple diagnostics are accumulated.

The current implementation uses:

```text
DiagnosticBuilder
```

The builder SHALL produce a canonical:

```text
DiagnosticReport
```

This avoids ad hoc mutable diagnostic accumulation throughout the resolution
pipeline.

---

## 23. Resolution Context Diagnostics

Some diagnostics require contextual information beyond a simple resolution
plan.

The diagnostics architecture exposes:

```text
ResolutionContext
```

and context-oriented adapter ports.

These MAY provide information required for:

- cycle detection;
- conflict detection;
- dependency relationships;
- additional resolution state.

Context adapters SHALL preserve architectural separation between diagnostic
generation and underlying resolution data sources.

---

## 24. Diagnostic Ports

The diagnostic subsystem SHALL expose explicit ports where diagnostic sources or
adapters depend on external resolution information.

Current public ports include:

```text
ConflictDetectionSource
CycleDetectionSource
ResolutionContextDiagnosticAdapter
ResolutionDiagnosticAdapter
```

Ports SHALL define architectural boundaries rather than concrete infrastructure
dependencies.

---

## 25. Diagnostic Explanation

Enriched diagnostics MAY be converted into human-oriented explanations.

The architecture exposes:

```text
ResolutionExplainer
ResolutionExplanation
```

Explanation behavior is rule-driven.

Current explanation rules include:

```text
MissingDependencyRule
VersionConflictRule
DependencyCycleRule
DefaultRule
```

The explanation layer SHALL NOT modify the underlying diagnostic.

It SHALL derive explanatory information from it.

---

## 26. Explanation Rule Registry

Explanation rules SHALL be discoverable through an explicit registry.

The current architecture exposes:

```text
ExplanationRule
ExplanationRuleRegistry
```

A registry selects a supporting rule for a diagnostic.

A default rule MAY provide fallback explanation behavior when no specialized
rule applies.

---

## 27. Diagnostic Suggestions

Diagnostics MAY produce remediation suggestions.

The architecture exposes:

```text
ResolutionSuggestion
SuggestionGenerator
```

Suggestions MAY recommend actions such as:

- installing a missing dependency;
- selecting a compatible version;
- removing a dependency cycle;
- correcting an invalid package;
- reviewing an unresolved plugin reference.

Suggestions SHALL be derived from structured diagnostics.

They SHALL NOT replace the underlying diagnostic evidence.

---

## 28. Diagnostic Formatting

Diagnostic explanations SHALL support multiple output formats.

The architecture currently exposes:

```text
ExplanationFormatter
TextExplanationFormatter
JsonExplanationFormatter
```

Text output is intended for human-readable environments.

JSON output is intended for machine-readable integration.

Formatting SHALL remain separate from diagnostic generation.

---

## 29. CLI Rendering

Diagnostics MAY be rendered through the command-line interface.

The current architecture exposes:

```text
DiagnosticCliRenderer
TerminalFormatter
```

CLI rendering SHALL operate on structured diagnostic or explanation models.

Business and resolution logic SHALL NOT depend on terminal formatting.

---

## 30. Determinism

Diagnostic generation SHALL be deterministic for equivalent resolution input.

Equivalent resolver state SHOULD produce equivalent:

- diagnostic kinds;
- diagnostic severities;
- canonical plugin identities;
- diagnostic paths;
- report error state.

Formatting MAY vary by selected renderer.

Underlying semantic diagnostics SHALL remain stable.

---

## 31. Architecture Boundaries

The diagnostic architecture has a deliberately separated responsibility.

```text
Version / Compatibility Resolution
            │
            ▼
Dependency Graph Resolution
            │
            ▼
Resolution Plan / Technical Diagnostics
            │
            ▼
Diagnostic Adapters
            │
            ▼
Plugin Resolution Diagnostics
            │
            ▼
Diagnostic Report
            │
            ├── Explain
            ├── Suggest
            ├── Format
            └── Render
```

RFC-0004 governs compatibility semantics.

RFC-0005 governs dependency graph structure and ordering.

RFC-0006 governs resolution diagnostic representation and transformation.

---

## 32. Security and Integrity

Diagnostic generation SHALL preserve canonical plugin identity.

Diagnostic paths SHALL NOT silently introduce alternate plugin identifiers.

Diagnostic adapters SHALL not change the semantic meaning of resolver failures.

Machine-readable diagnostic classifications SHALL remain independent from
human-readable formatting.

Diagnostics SHALL avoid exposing unrelated sensitive runtime information.

---

## 33. Compatibility

Legacy Plugin Identifier aliases MAY be accepted before diagnostic
normalization.

Once stored in a diagnostic model, plugin identity SHALL be canonicalized.

Legacy aliases SHALL NOT create parallel diagnostic identities.

Diagnostic code and kind evolution SHOULD preserve compatibility where
practical.

Breaking diagnostic contract changes SHALL require explicit architectural
governance.

---

## 34. Implementation Mapping

The current FamilyOS implementation maps this RFC primarily to:

```text
src/familyos_cli/plugins/ecosystem/resolution/
src/familyos_cli/plugins/ecosystem/diagnostics/
```

Primary technical diagnostic components include:

```text
ResolutionDiagnostic
ResolutionDiagnosticCode
ResolutionDiagnosticSeverity
```

Primary enriched diagnostic components include:

```text
PluginResolutionDiagnostic
DiagnosticKind
DiagnosticSeverity
DiagnosticReport
DiagnosticBuilder
DiagnosticPipeline
```

Additional public diagnostic capabilities include:

```text
ConflictDiagnosticAdapter
CycleDiagnosticAdapter
ResolutionConflictAdapter
ResolutionConflictDiagnosticAdapter
ResolutionCycleDiagnosticAdapter
ConflictDetector
CycleDetector
ResolutionExplainer
ResolutionExplanation
SuggestionGenerator
ResolutionSuggestion
TextExplanationFormatter
JsonExplanationFormatter
DiagnosticCliRenderer
TerminalFormatter
```

Implementation names MAY evolve.

The semantic contracts defined by this RFC SHALL remain stable unless changed
through explicit RFC or ADR governance.

---

## 35. Validation

The implementation SHALL be validated for at least:

- technical diagnostic construction;
- diagnostic code values;
- technical severity values;
- canonical plugin identity;
- enriched diagnostic construction;
- diagnostic kinds;
- enriched severity values;
- diagnostic paths;
- immutable diagnostic reports;
- report severity filtering;
- report success and error semantics;
- conflict adaptation;
- dependency cycle adaptation;
- diagnostic pipeline behavior;
- explanation rules;
- explanation rule registry;
- remediation suggestions;
- text formatting;
- JSON formatting;
- CLI rendering.

The current implementation provides dedicated diagnostics coverage under:

```text
tests/unit/plugins/ecosystem/diagnostics/
```

The audited baseline is:

```text
107 passed
```

The diagnostics source tree also passes:

```text
ruff check src/familyos_cli/plugins/ecosystem/diagnostics
```

---

## 36. Normative References

- ADR-0007 — Official Plugins Architecture
- ADR-0008 — Specification-Driven Platform
- ADR-0009 — Normative Validation Architecture
- RFC-0004 — Plugin Versioning & Compatibility
- RFC-0005 — Plugin Dependency Graph

---

## 37. Decision

FamilyOS SHALL represent plugin resolution problems through structured
diagnostics.

Technical resolver diagnostics SHALL remain distinct from enriched plugin-facing
diagnostics.

Diagnostic identity SHALL preserve canonical Plugin Identifier semantics.

Diagnostic adapters SHALL translate resolution information into enriched
diagnostics.

Diagnostic reports SHALL aggregate diagnostics immutably.

Diagnostics MAY be explained, transformed into suggestions, formatted, and
rendered without coupling those presentation concerns to plugin resolution
logic.

---

## Revision History

| Version | Date | Description |
| --- | --- | --- |
| 1.0.0 | 2026-08-12 | Canonical publication replacing the historical RFC-000AC placeholder identifier. |
