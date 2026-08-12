# RFC-0005 — Plugin Dependency Graph

## Status

Accepted

## Title

Plugin Dependency Graph

## Summary

This RFC defines the canonical dependency graph model used by the FamilyOS
plugin ecosystem.

The dependency graph represents resolved relationships between concrete plugin
packages and provides the structural foundation for deterministic plugin
dependency resolution.

It defines:

- canonical graph identity;
- graph nodes and dependency edges;
- graph construction from plugin manifests;
- compatible dependency target selection;
- dependency cycle detection;
- deterministic topological ordering;
- dependency graph resolution;
- resolution diagnostics.

Version constraint semantics and package compatibility rules remain governed by
RFC-0004 — Plugin Versioning & Compatibility.

---

## 1. Context

FamilyOS plugins may depend on other plugins.

Dependency declarations originate in plugin manifests and identify their target
using a canonical Plugin Identifier together with an independent version
constraint.

Dependency declarations must eventually be transformed into a concrete,
versioned dependency structure suitable for deterministic installation and
runtime preparation.

A flat collection of dependency declarations is insufficient for this purpose.

FamilyOS therefore models resolved plugin relationships as a directed
dependency graph.

---

## 2. Goals

This RFC defines the canonical architecture for plugin dependency graphs.

The dependency graph SHALL provide:

1. canonical plugin identity;
2. concrete versioned graph nodes;
3. directed dependency relationships;
4. deterministic graph construction;
5. compatible dependency target selection;
6. dependency cycle detection;
7. deterministic dependency-first ordering;
8. structured resolution results;
9. integration with plugin resolution diagnostics.

---

## 3. Non-Goals

This RFC does not redefine:

- Plugin Identifier syntax;
- plugin manifest format;
- semantic versioning;
- version constraint syntax;
- package compatibility policy;
- plugin discovery;
- package distribution;
- installation mechanics;
- runtime lifecycle semantics.

Those concerns belong to their respective specifications, ADRs, and RFCs.

In particular:

- RFC-0003 governs Plugin Discovery & Distribution;
- RFC-0004 governs Plugin Versioning & Compatibility.

---

## 4. Dependency Graph Model

The FamilyOS plugin dependency graph is a directed graph.

Conceptually:

```text
PluginDependencyGraph
    ├── PluginNode
    ├── PluginNode
    └── DependencyEdge
```

Each node represents one concrete plugin package.

Each edge represents one resolved dependency declaration.

If plugin A depends on plugin B:

```text
A ─────► B
```

the edge direction is:

```text
dependent ─────► dependency
```

This direction is normative.

It allows dependency-first ordering to place B before A.

---

## 5. Plugin Node

A graph node SHALL represent one concrete `PluginPackage`.

The canonical implementation model is:

```text
PluginNode
    └── package
```

A node exposes:

```text
plugin_id
version
identifier()
```

`PluginNode.plugin_id` SHALL expose the canonical Plugin Identifier.

Example:

```text
familyos.security
```

`PluginNode.version` SHALL expose the package version.

Example:

```text
1.2.0
```

Concrete node identity SHALL be derived from the package identifier.

Conceptually:

```text
Plugin Identifier + Version
```

Example:

```text
familyos.security@1.2.0
```

Multiple versions of the same logical plugin MAY therefore exist as distinct
candidate nodes.

---

## 6. Canonical Plugin Identity

Logical dependency graph identity SHALL use the canonical Plugin Identifier.

Example:

```text
familyos.security
familyos.health
familyos.finance
```

Graph construction SHALL NOT use human-readable display names as plugin
identity.

A historical `name` property MAY remain available as a compatibility alias.

When present:

```text
PluginNode.name
```

SHALL represent exactly the same logical Plugin Identifier as:

```text
PluginNode.plugin_id
```

It SHALL NOT establish a second identity namespace.

---

## 7. Dependency Edge

A dependency edge SHALL connect:

```text
source
target
dependency
```

where:

- `source` is the dependent plugin package;
- `target` is the selected dependency package;
- `dependency` preserves the originating dependency declaration.

Conceptually:

```text
DependencyEdge
    ├── source: PluginNode
    ├── target: PluginNode
    └── dependency: PluginDependency
```

Example:

```text
familyos.education@1.0.0
        │
        └────► familyos.security@1.2.0
```

The edge SHALL preserve the semantic relationship between the original
dependency declaration and the concrete package selected to satisfy it.

---

## 8. Graph Identity and Uniqueness

A graph SHALL identify concrete nodes using their package identifier.

Adding the same concrete node more than once SHALL NOT create duplicate logical
nodes.

Dependency edges SHALL behave as a set of resolved relationships.

Graph operations SHALL preserve canonical package and Plugin Identifier
semantics.

---

## 9. Graph Construction

`DependencyGraphBuilder` is responsible for transforming plugin manifests into
a concrete dependency graph.

Graph construction SHALL occur in two logical phases:

```text
Plugin Manifests
      │
      ▼
Create Nodes
      │
      ▼
Resolve Dependency Targets
      │
      ▼
Create Edges
      │
      ▼
Plugin Dependency Graph
```

All manifest packages SHALL first become candidate graph nodes.

Dependency declarations SHALL then be resolved against those candidate nodes.

---

## 10. Dependency Target Selection

A dependency declaration identifies its target using:

```text
PluginDependency.plugin_id
```

and an independent version constraint.

Candidate packages SHALL first be grouped by canonical Plugin Identifier.

The graph builder SHALL delegate compatible package selection to the package
selection policy used by the plugin resolution subsystem.

When multiple compatible versions exist, the selected package SHALL follow the
canonical compatibility and version selection rules.

The current implementation selects the highest compatible package.

The detailed semantics governing version compatibility remain defined by
RFC-0004.

If no compatible package can be selected, graph construction SHALL NOT invent a
dependency target.

Missing or incompatible dependencies SHALL be handled by the surrounding
resolution and diagnostic architecture.

---

## 11. Dependency Cycle Detection

A valid dependency graph intended for dependency-first resolution SHALL be
acyclic.

Examples of invalid cycles include:

```text
A ─► A
```

and:

```text
A ─► B
▲    │
└────┘
```

and:

```text
A ─► B ─► C
▲         │
└─────────┘
```

`CycleDetector` SHALL detect dependency cycles, including:

- self-dependencies;
- two-node cycles;
- multi-node cycles;
- cycles contained in disconnected graph components.

Shared dependencies SHALL NOT be interpreted as cycles.

Example:

```text
A ─► C
B ─► C
```

is valid.

---

## 12. Topological Ordering

An acyclic dependency graph SHALL support deterministic topological ordering.

The required ordering is dependency-first.

Given:

```text
A ─► B
B ─► C
```

the resulting order SHALL be:

```text
C
B
A
```

Every dependency SHALL appear before every dependent plugin that requires it.

When several nodes are simultaneously eligible for ordering, FamilyOS SHALL
apply deterministic ordering based on concrete node identity.

The current implementation uses the node identifier as the deterministic
ordering key.

A topological sort attempted on a cyclic graph SHALL fail.

---

## 13. Dependency Graph Resolution

`DependencyGraphResolver` coordinates structural graph resolution.

The canonical resolution sequence is:

```text
PluginDependencyGraph
        │
        ▼
Cycle Detection
        │
        ├── cycle detected
        │       │
        │       ▼
        │   Failed Result
        │
        └── acyclic
                │
                ▼
        Topological Sort
                │
                ▼
        Dependency-First Order
                │
                ▼
        Successful Result
```

Cycle detection SHALL occur before topological sorting.

A graph containing a cycle SHALL NOT produce an installation order.

---

## 14. Resolution Result

Dependency graph resolution SHALL return a structured result.

The canonical result contains:

```text
DependencyResolutionResult
    ├── ordered_nodes
    ├── cycle_detected
    └── diagnostics
```

A successful resolution SHALL provide dependency-first ordered nodes.

A cyclic resolution SHALL:

- provide no ordered nodes;
- set `cycle_detected` to true;
- expose an error diagnostic.

The canonical diagnostic code for this condition is:

```text
cycle_detected
```

---

## 15. Diagnostics Integration

Dependency graph failures SHALL integrate with the FamilyOS plugin resolution
diagnostic architecture.

A dependency cycle SHALL be representable as a structured resolution
diagnostic rather than only as an implementation exception.

Diagnostics MAY subsequently be:

- normalized;
- explained;
- rendered through the CLI;
- transformed into remediation suggestions.

Detailed diagnostic presentation and user experience remain outside the scope
of this RFC.

---

## 16. Determinism

Dependency graph behavior SHALL be deterministic for equivalent inputs.

Determinism applies to:

- concrete dependency target selection;
- graph node identity;
- dependency-first ordering;
- diagnostic outcomes.

Equivalent manifest and package inputs SHALL NOT produce arbitrary installation
orders.

This property is required for reproducible plugin resolution and predictable
FamilyOS environments.

---

## 17. Architecture Boundaries

The dependency graph has a deliberately narrow responsibility.

```text
Discovery
    │
    ▼
Available Packages
    │
    ▼
Version / Compatibility Resolution
    │
    ▼
Dependency Graph
    │
    ├── Nodes
    ├── Edges
    ├── Cycle Detection
    └── Topological Ordering
    │
    ▼
Installation / Runtime Preparation
```

RFC-0003 governs how plugin packages are discovered and distributed.

RFC-0004 governs version constraints and compatibility.

RFC-0005 governs the concrete graph representation and structural ordering of
resolved dependencies.

These responsibilities SHALL remain conceptually distinct.

---

## 18. Security and Integrity

Dependency graph construction SHALL preserve the identity of packages selected
during resolution.

Graph construction SHALL NOT silently rewrite canonical Plugin Identifiers.

A dependency edge SHALL refer only to an actual selected package represented by
a graph node.

Dependency cycles SHALL be rejected before an installation or activation order
is accepted.

These properties prevent ambiguous dependency execution and inconsistent
runtime preparation.

---

## 19. Compatibility

Legacy Plugin Identifier aliases MAY be accepted by compatibility layers before
or during dependency normalization.

Once represented in the canonical dependency graph, logical plugin identity
SHALL use canonical Plugin Identifiers.

Legacy aliases SHALL NOT create parallel logical graph identities.

For example:

```text
security
```

and:

```text
familyos.security
```

SHALL NOT become independent logical plugins when the former is recognized as a
legacy alias of the latter.

---

## 20. Implementation Mapping

The current FamilyOS implementation maps this RFC to:

```text
src/familyos_cli/plugins/ecosystem/dependency_graph/
```

Primary implementation components include:

```text
PluginNode
DependencyEdge
PluginDependencyGraph
DependencyGraphBuilder
CycleDetector
TopologicalSorter
DependencyGraphResolver
DependencyResolutionResult
```

The public dependency graph API currently exposes:

```text
CycleDetector
DependencyEdge
DependencyGraphBuilder
PluginDependencyGraph
PluginNode
TopologicalSorter
```

Implementation property names MAY evolve.

The semantic contracts defined by this RFC SHALL remain stable unless changed
through explicit RFC or ADR governance.

---

## 21. Validation

The implementation SHALL be validated for at least:

- graph node identity;
- dependency edge semantics;
- graph node uniqueness;
- graph construction;
- dependency package selection;
- missing dependency behavior;
- self-cycle detection;
- multi-node cycle detection;
- disconnected-component cycle detection;
- acyclic graphs;
- deterministic topological sorting;
- dependency-first ordering;
- cyclic resolution failure;
- structured cycle diagnostics.

The current implementation provides dedicated unit coverage under:

```text
tests/unit/plugins/ecosystem/dependency_graph/
```

---

## 22. Normative References

- ADR-0007 — Official Plugins Architecture
- RFC-0003 — Plugin Discovery & Distribution
- RFC-0004 — Plugin Versioning & Compatibility

---

## 23. Decision

FamilyOS SHALL use a directed, version-aware dependency graph as the canonical
structural representation of resolved plugin dependencies.

Logical plugin identity SHALL use canonical Plugin Identifiers.

Concrete graph nodes SHALL represent versioned plugin packages.

Dependency edges SHALL point from dependent plugins to their dependencies.

Dependency graph resolution SHALL reject cycles and SHALL produce deterministic
dependency-first ordering for acyclic graphs.

---

## Revision History

| Version | Date | Description |
| --- | --- | --- |
| 1.0.0 | 2026-08-12 | Canonical publication replacing the historical RFC-000AB placeholder identifier. |
