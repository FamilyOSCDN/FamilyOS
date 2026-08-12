# RFC-0004 — Plugin Versioning & Compatibility

## Context

The FamilyOS plugin ecosystem is designed for independent evolution.

A plugin is not assumed to be released in lockstep with the FamilyOS core or
with every other plugin. This independence is essential for an extensible
platform, but it creates a compatibility problem: at any point in time, several
versions of a plugin may exist and another plugin may accept only a subset of
them.

For example, the ecosystem may contain:

```text
familyos.documents 1.3.0
familyos.documents 1.4.0
familyos.documents 1.8.2
familyos.documents 2.0.0
```

while another plugin declares:

```text
familyos.documents >=1.4.0,<2.0.0
```

The platform must determine that `1.4.0` and `1.8.2` are compatible while
`1.3.0` and `2.0.0` are not.

That decision is not a repository concern, a CLI concern, or a dependency graph
traversal concern. It is a version-domain concern.

## Existing FamilyOS Architecture

The current plugin architecture already separates the relevant stages:

```text
Plugin Manifest
      |
      v
Discovery
      |
      v
Available Plugin Packages
      |
      v
Version Compatibility
      |
      v
Dependency Resolution
      |
      +------------------+
      |                  |
      v                  v
Resolved Graph      Diagnostics
```

The platform already implements the core value objects required by RFC-0004:

```text
PluginVersion
VersionOperator
VersionConstraint
ConstraintSet
```

These objects are consumed by package selection, plugin resolution, dependency
graph construction, and diagnostics.

RFC-0004 therefore documents and governs an existing capability rather than
introducing an unrelated replacement architecture.

## Why Versioning Must Be Explicit

Treating versions as arbitrary strings would make ordering incorrect.

For example, lexical ordering does not reliably express:

```text
1.9.0 < 1.10.0
```

and cannot express pre-release precedence such as:

```text
1.0.0-alpha < 1.0.0-beta < 1.0.0
```

Likewise, dependency expressions such as:

```text
^2.3.4
~2.3.4
>=1.4.0,<2.0.0
```

require stable semantics.

If different components interpret those expressions differently, FamilyOS can
produce contradictory outcomes: a package selector may accept a package that a
diagnostic layer later reports as incompatible.

RFC-0004 prevents that semantic drift.

## Relationship to Discovery

RFC-0003 governs discovery and distribution.

Discovery is responsible for making package candidates available. It may read
version text from package metadata, but it SHALL NOT define a second
compatibility model.

RFC-0004 starts when a version string or dependency constraint needs semantic
interpretation.

## Relationship to Dependency Resolution

RFC-0005 governs dependency graph structure and resolution.

A resolver may receive several candidates for one plugin identity. It relies on
RFC-0004 to determine which candidates satisfy the requested constraints.

RFC-0005 may then apply a graph-level policy such as selecting the highest
compatible candidate.

The distinction is intentional:

```text
RFC-0004
  version parsing
  precedence
  constraint evaluation
  compatibility

RFC-0005
  dependency graph
  candidate traversal
  selection
  cycles
  resolution result
```

## Relationship to Diagnostics

RFC-0006 governs resolution diagnostics.

If no package satisfies a constraint set, RFC-0004 determines the underlying
compatibility result, RFC-0005 determines that resolution failed, and RFC-0006
represents that failure.

Diagnostics SHALL report the same semantics used by the resolver.

## Domain Independence

Compatibility evaluation must remain independent from:

- filesystem layout;
- repository implementation;
- package transport;
- network access;
- CLI commands;
- terminal rendering;
- operating-system state;
- plugin lifecycle state.

That makes the versioning model deterministic, reusable, and testable.

## Architectural Invariant

RFC-0004 establishes the following invariant:

```text
For the same valid PluginVersion and the same VersionConstraint or
ConstraintSet, every conforming FamilyOS component SHALL produce the same
compatibility result.
```

This invariant is the reason versioning is defined as a dedicated domain
contract.
