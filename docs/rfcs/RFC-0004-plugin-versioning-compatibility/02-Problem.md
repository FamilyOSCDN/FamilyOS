# RFC-0004 — Plugin Versioning & Compatibility

## Problem Statement

Independent plugin releases create multiple classes of ambiguity unless
version semantics are centralized.

### Version Representation

The platform needs to distinguish:

```text
1.4.0
1.4.1
1.4.1-alpha
1.4.1-alpha.2
1.4.1+build.17
```

These values cannot be treated as opaque strings because dependency resolution
requires comparison and ordering.

### Invalid Versions

Malformed version strings must not silently participate in resolution.

Examples of invalid forms must be rejected at the version-domain boundary
rather than handled differently by downstream components.

### Version Precedence

The platform needs a deterministic ordering.

For stable versions:

```text
1.2.3 < 1.2.4 < 1.3.0 < 2.0.0
```

For pre-release versions:

```text
1.0.0-alpha < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

A resolver cannot select the highest compatible package if precedence is not
defined centrally.

### Build Metadata

Build metadata distinguishes representations such as:

```text
1.5.0+build.10
1.5.0+build.11
```

but must not alter precedence.

The system therefore needs a distinction between representation equality and
semantic precedence.

### Constraint Language

Plugins need a compact way to declare requirements:

```text
==1.4.0
>=1.4.0
<2.0.0
^2.3.4
~2.3.4
>=1.4.0,<2.0.0
```

These expressions need one canonical interpretation.

### Zero-Major Caret Semantics

Caret ranges require special treatment when major version is zero.

The following are intentionally different:

```text
^2.3.4   -> >=2.3.4,<3.0.0
^0.3.4   -> >=0.3.4,<0.4.0
^0.0.4   -> >=0.0.4,<0.0.5
```

Without explicit rules, zero-major compatibility becomes ambiguous.

### Compound Constraints

A constraint set such as:

```text
>=1.4.0,<2.0.0
```

must have defined composition semantics.

RFC-0004 defines conjunction: both conditions must hold.

### Cross-Layer Duplication

Version rules are needed by:

- manifests;
- package selectors;
- resolvers;
- dependency graph builders;
- diagnostics;
- tests.

Duplicating those rules would make semantic divergence likely.

### Failure Modes

Without RFC-0004, FamilyOS risks:

- inconsistent version ordering;
- invalid versions entering resolution;
- incompatible packages being accepted;
- compatible packages being rejected;
- contradictory diagnostics;
- different meanings for caret or tilde operators;
- unstable package selection;
- duplicated compatibility code;
- difficult future migration.

## Required Property

FamilyOS needs one pure domain-level compatibility decision:

```text
candidate version + constraint set -> compatible | incompatible
```

RFC-0004 defines that decision.
