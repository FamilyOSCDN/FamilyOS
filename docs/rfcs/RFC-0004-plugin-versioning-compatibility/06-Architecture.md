# RFC-0004 — Plugin Versioning & Compatibility

## Architecture

RFC-0004 uses a deliberately small domain architecture.

```text
                     PluginVersion
                    /             \
                   v               v
          VersionOperator    VersionConstraint
                                   |
                                   v
                             ConstraintSet
                                   |
                                   v
                        Compatibility Result
                                   |
                                   v
                               RFC-0005
```

## PluginVersion

`PluginVersion` owns:

- semantic version parsing;
- validation;
- canonical string formatting;
- pre-release representation;
- build metadata representation;
- precedence comparison.

It does not own dependency graph behavior.

## VersionOperator

`VersionOperator` enumerates supported comparison semantics.

It is intentionally explicit so unsupported expressions are rejected instead
of interpreted heuristically.

## VersionConstraint

`VersionConstraint` combines one operator and one reference version.

It owns evaluation of an atomic requirement.

Conceptually:

```text
VersionConstraint.is_satisfied_by(candidate)
```

## ConstraintSet

`ConstraintSet` aggregates one or more atomic constraints.

Its semantics are conjunctive:

```text
all(constraint.is_satisfied_by(candidate) for constraint in constraints)
```

## Architectural Boundary

The versioning domain SHALL remain independent from:

- repositories;
- filesystem concerns;
- networking;
- CLI frameworks;
- terminal rendering;
- runtime lifecycle.

Package selection and dependency graph resolution belong to higher layers.

This structure keeps compatibility rules easy to test and difficult to
accidentally redefine.
