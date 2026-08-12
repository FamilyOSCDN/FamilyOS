# RFC-0004 — Plugin Versioning & Compatibility

## Testing

RFC-0004 requires direct tests of the domain model and integration tests where
resolution consumes version semantics.

## PluginVersion Tests

Required cases include:

- stable version parsing;
- pre-release parsing;
- build metadata parsing;
- invalid version rejection;
- non-negative component validation;
- numeric pre-release leading-zero rejection;
- canonical string rendering;
- core precedence;
- stable vs pre-release precedence;
- numeric pre-release comparison;
- lexical pre-release comparison;
- build metadata precedence neutrality.

## VersionOperator Tests

Tests SHALL verify the canonical textual value of every supported operator.

## VersionConstraint Tests

Each operator SHALL have positive and negative cases.

Caret tests SHALL cover:

```text
major > 0
major == 0, minor > 0
major == 0, minor == 0
```

Tilde tests SHALL verify the next-minor exclusive upper bound.

## ConstraintSet Tests

Tests SHALL cover:

- parsing;
- whitespace normalization;
- empty input rejection;
- conjunctive evaluation;
- mixed lower/upper bounds.

## Integration Tests

Higher-level tests SHOULD verify:

- package filtering;
- highest-compatible selection;
- incompatible candidate handling;
- resolver failure when no compatible version exists;
- diagnostic mapping.

## Quality Gates

The repository SHALL run:

```text
ruff
mypy
pytest
```

before RFC closure.
