# RFC-0004 — Plugin Versioning & Compatibility

## Goals

RFC-0004 SHALL establish a single canonical plugin versioning model.

The RFC has the following goals.

### G1 — Structured Versions

Plugin versions SHALL be represented as structured values rather than opaque
strings.

### G2 — Deterministic Parsing

The platform SHALL accept canonical semantic version strings and reject invalid
ones.

### G3 — Deterministic Precedence

The platform SHALL define total ordering semantics appropriate for package
selection.

### G4 — Pre-release Semantics

Pre-release versions SHALL compare deterministically and SHALL have lower
precedence than the corresponding stable version.

### G5 — Build Metadata Semantics

Build metadata SHALL be preserved but SHALL NOT affect precedence.

### G6 — Explicit Constraint Operators

FamilyOS SHALL use a bounded set of explicit operators:

```text
==
>
>=
<
<=
^
~
```

### G7 — Compatibility Ranges

Caret and tilde constraints SHALL have deterministic exclusive upper bounds.

### G8 — Compound Requirements

Constraint sets SHALL support multiple atomic constraints with logical AND
semantics.

### G9 — Reusable Compatibility

Compatibility SHALL be represented as reusable domain behavior that can be
consumed by package selection and dependency resolution.

### G10 — Layer Separation

Discovery, dependency graphs, diagnostics, and CLI presentation SHALL consume
RFC-0004 semantics rather than redefining them.

### G11 — Testability

Boundary conditions SHALL be directly testable without infrastructure.

### G12 — Long-Term Governance

Changes that alter compatibility results SHALL be treated as architectural
changes and reviewed explicitly.
