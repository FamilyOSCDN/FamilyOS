# RFC-0004 — Plugin Versioning & Compatibility

## Semantic Versioning

FamilyOS plugin versions follow Semantic Versioning-compatible precedence.

## Core Precedence

```text
1.0.0 < 1.0.1
1.0.9 < 1.1.0
1.9.9 < 2.0.0
```

## Pre-release Precedence

A pre-release has lower precedence than the corresponding stable release:

```text
1.0.0-alpha < 1.0.0
```

Representative ordering:

```text
1.0.0-alpha
<
1.0.0-alpha.1
<
1.0.0-beta
<
1.0.0-rc.1
<
1.0.0
```

## Identifier Comparison

When comparing two pre-release sequences:

1. compare identifiers from left to right;
2. equal identifiers continue to the next position;
3. numeric vs numeric compares integer value;
4. numeric < non-numeric;
5. non-numeric values compare lexically;
6. if all common identifiers are equal, the shorter sequence has lower
   precedence.

## Build Metadata

Build metadata is excluded from precedence.

Therefore:

```text
1.2.3+build.1
1.2.3+build.2
```

have equal precedence.

## Compatibility Consequence

Constraint evaluation relies on precedence. Any change to precedence semantics
can change dependency resolution and is therefore an architectural change.
