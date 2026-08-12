# RFC-0004 — Plugin Versioning & Compatibility

## Domain Model

## PluginVersion

`PluginVersion` is an immutable comparable value object.

Conceptual state:

```text
major: int
minor: int
patch: int
pre_release: tuple[str, ...]
build_metadata: tuple[str, ...]
```

Its equality semantics reflect semantic precedence and therefore exclude build
metadata.

Its string representation includes build metadata when present.

## VersionOperator

Canonical operators:

```text
EQUAL             ==
GREATER           >
GREATER_OR_EQUAL  >=
LOWER             <
LOWER_OR_EQUAL    <=
COMPATIBLE        ^
APPROXIMATE       ~
```

## VersionConstraint

Conceptual state:

```text
operator: VersionOperator
version: PluginVersion
```

The object answers whether a candidate version satisfies the atomic
requirement.

## ConstraintSet

Conceptual state:

```text
constraints: tuple[VersionConstraint, ...]
```

The set SHALL NOT be empty when parsed from textual input.

The candidate must satisfy every member.

## Invariants

- versions are valid at construction;
- constraints contain a supported operator;
- constraints contain a valid reference version;
- constraint sets parsed from text contain at least one constraint;
- compatibility evaluation is pure and deterministic.
