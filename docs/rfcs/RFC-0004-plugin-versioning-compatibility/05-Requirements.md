# RFC-0004 — Plugin Versioning & Compatibility

## Requirements

## R1 — Canonical Version Shape

A version SHALL contain:

- major;
- minor;
- patch;
- optional pre-release identifiers;
- optional build metadata.

The canonical textual shape SHALL be:

```text
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

## R2 — Numeric Components

Major, minor, and patch SHALL be non-negative integers.

## R3 — Pre-release Validation

Pre-release identifiers SHALL NOT be empty.

Numeric pre-release identifiers SHALL NOT contain leading zeroes.

## R4 — Build Metadata Validation

Build metadata identifiers SHALL NOT be empty.

## R5 — Parsing

Invalid semantic version strings SHALL raise a validation error rather than be
coerced or partially interpreted.

## R6 — Precedence

Version precedence SHALL compare:

1. major;
2. minor;
3. patch;
4. pre-release identifiers.

Build metadata SHALL NOT participate in precedence.

## R7 — Stable vs Pre-release

A stable version SHALL have higher precedence than a pre-release with the same
major, minor, and patch.

## R8 — Supported Operators

The supported constraint operators SHALL be:

```text
==
>
>=
<
<=
^
~
```

## R9 — Atomic Constraint

An atomic constraint SHALL contain exactly one supported operator and one valid
reference version.

## R10 — Caret

Caret compatibility SHALL use the first significant version component to
calculate an exclusive upper bound.

## R11 — Tilde

Tilde compatibility SHALL use the next minor version as the exclusive upper
bound.

## R12 — Compound Constraints

A non-empty comma-separated constraint expression SHALL produce a
`ConstraintSet`.

All contained constraints SHALL be satisfied for the candidate to be
compatible.

## R13 — Determinism

Compatibility SHALL not depend on discovery order, repository source, runtime
state, or presentation.

## R14 — Reuse

Package selectors and dependency resolvers SHALL consume these contracts rather
than duplicate their semantics.
