# RFC-0004 — Plugin Versioning & Compatibility

## Status

Accepted

## Purpose

RFC-0004 defines the canonical versioning and compatibility semantics for the
FamilyOS plugin ecosystem.

## Document Set

| # | Document | Purpose |
|---|---|---|
| 00 | `00-Abstract.md` | Normative overview |
| 01 | `01-Context.md` | Architectural context |
| 02 | `02-Problem.md` | Problem definition |
| 03 | `03-Goals.md` | Goals |
| 04 | `04-Non-Goals.md` | Explicit exclusions |
| 05 | `05-Requirements.md` | Normative requirements |
| 06 | `06-Architecture.md` | Architecture |
| 07 | `07-Domain-Model.md` | Domain contracts |
| 08 | `08-Version-Model.md` | Version representation |
| 09 | `09-Version-Constraints.md` | Constraint language |
| 10 | `10-Resolution-Algorithm.md` | Compatibility evaluation |
| 11 | `11-Semantic-Versioning.md` | Precedence semantics |
| 12 | `12-Compatibility.md` | Compatibility ranges |
| 13 | `13-CLI.md` | CLI boundary |
| 14 | `14-Implementation-Plan.md` | Implementation/stabilization plan |
| 15 | `15-Migration.md` | RFC-000AA migration |
| 16 | `16-Testing.md` | Validation strategy |
| 17 | `17-Alternatives.md` | Rejected alternatives |
| 18 | `18-Open-Questions.md` | Future questions |
| 19 | `19-Decisions.md` | Canonical decisions |
| 20 | `20-Future-Work.md` | Future evolution |

## Canonical Contracts

```text
PluginVersion
VersionOperator
VersionConstraint
ConstraintSet
```

## Architectural Position

```text
RFC-0003 — Plugin Discovery & Distribution
                    |
                    v
RFC-0004 — Plugin Versioning & Compatibility
                    |
                    v
RFC-0005 — Plugin Dependency Graph
                    |
                    v
RFC-0006 — Plugin Resolution Diagnostics
```

## Validation Expectations

RFC-0004 closure requires:

- no draft placeholders;
- canonical RFC-0004 references;
- version and constraint tests passing;
- dependency-resolution integration tests passing;
- Ruff passing;
- MyPy passing;
- Pytest passing;
- `git diff --check` passing.

## Revision History

| Version | Date | Description |
|---|---|---|
| 1.0.0 | 2026-08-12 | Reconstructed complete canonical RFC-0004 documentation from the implemented FamilyOS plugin versioning and compatibility model. |
