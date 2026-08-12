# RFC-0004 — Plugin Versioning & Compatibility

## Implementation Plan

The core RFC-0004 capability is already implemented.

The implementation plan is therefore a stabilization and governance plan.

## Phase 1 — Core Version Value

Maintain `PluginVersion` as the canonical semantic version representation.

Validation SHALL cover:

- canonical parsing;
- invalid values;
- pre-release rules;
- build metadata;
- ordering.

## Phase 2 — Constraint Operators

Maintain the supported operator set in `VersionOperator`.

New operators SHALL NOT be introduced without explicit semantics and tests.

## Phase 3 — Atomic Constraints

Maintain `VersionConstraint` as the canonical atomic compatibility predicate.

Boundary tests SHALL cover every operator.

## Phase 4 — Compound Constraints

Maintain `ConstraintSet` as a conjunction of atomic requirements.

## Phase 5 — Resolution Consumption

Package selection and dependency resolution SHALL consume the canonical
objects.

## Phase 6 — Diagnostics

Resolution failures caused by version incompatibility SHALL be mapped into the
diagnostic architecture without redefining compatibility.

## Phase 7 — Documentation Closure

The historical placeholders are replaced by this complete RFC documentation.

Repository-wide quality gates SHALL remain green before closure.
