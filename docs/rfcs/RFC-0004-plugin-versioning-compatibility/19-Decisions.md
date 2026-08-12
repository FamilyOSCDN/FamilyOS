# RFC-0004 — Plugin Versioning & Compatibility

## Decisions

### D1

FamilyOS plugin versions use a Semantic Versioning-compatible model.

### D2

`PluginVersion` is the canonical version value object.

### D3

Build metadata is preserved but excluded from precedence.

### D4

Pre-release identifiers participate in precedence.

### D5

The supported operators are:

```text
== > >= < <= ^ ~
```

### D6

`VersionConstraint` owns atomic compatibility evaluation.

### D7

`ConstraintSet` uses logical AND semantics.

### D8

Caret compatibility uses the first significant version component to establish
the exclusive upper bound.

### D9

Tilde compatibility uses the next minor version as its exclusive upper bound.

### D10

Invalid versions and constraints are rejected rather than coerced.

### D11

Discovery and repositories do not define compatibility semantics.

### D12

RFC-0005 consumes RFC-0004 semantics for dependency resolution.

### D13

RFC-0006 consumes resolution outcomes for diagnostics.

### D14

Any change that alters compatibility results requires explicit architectural
governance.
