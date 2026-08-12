# RFC-0004 — Plugin Versioning & Compatibility

## Status

Accepted

## Abstract

RFC-0004 defines the canonical versioning and compatibility semantics used by
the FamilyOS plugin ecosystem.

FamilyOS plugins evolve independently. The platform may discover several
versions of the same plugin while dependent plugins declare exact versions,
lower or upper bounds, or compatibility ranges. The platform therefore needs
one deterministic interpretation of:

- plugin version strings;
- semantic version precedence;
- pre-release identifiers;
- build metadata;
- exact and ordered constraints;
- caret compatibility;
- tilde compatibility;
- compound version constraints;
- compatibility evaluation.

The canonical implementation is based on the following domain contracts:

```text
PluginVersion
VersionOperator
VersionConstraint
ConstraintSet
```

A plugin version uses the canonical form:

```text
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

Examples:

```text
1.0.0
1.4.2
2.0.0-alpha
2.0.0-alpha.3
2.0.0-rc.1+build.42
```

The supported constraint operators are:

```text
==
>
>=
<
<=
^
~
```

A `ConstraintSet` combines atomic constraints using logical AND semantics.

For example:

```text
>=1.4.0,<2.0.0
```

is satisfied only by a candidate version that satisfies both bounds.

Caret compatibility is defined by the first significant version component:

```text
^2.3.4   -> >=2.3.4,<3.0.0
^0.3.4   -> >=0.3.4,<0.4.0
^0.0.4   -> >=0.0.4,<0.0.5
```

Tilde compatibility permits updates within the same minor release line:

```text
~2.3.4   -> >=2.3.4,<2.4.0
```

Pre-release identifiers participate in precedence. A stable version has higher
precedence than the corresponding pre-release version.

Build metadata is preserved as part of the canonical string representation but
does not affect version precedence.

The architectural position of RFC-0004 is:

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

RFC-0003 answers which packages are available.

RFC-0004 answers what their versions and constraints mean.

RFC-0005 consumes those semantics during dependency graph construction and
candidate selection.

RFC-0006 represents and explains failures when no compatible resolution can be
produced.

RFC-0004 therefore isolates version compatibility as an explicit domain
capability rather than allowing its semantics to be duplicated across
discovery, resolution, diagnostics, or CLI presentation.

## Normative Outcome

A conforming FamilyOS component evaluating the same candidate version against
the same constraint set SHALL reach the same result.

That invariant is the core outcome of this RFC.
