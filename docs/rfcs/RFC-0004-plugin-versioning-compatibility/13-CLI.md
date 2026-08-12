# RFC-0004 — Plugin Versioning & Compatibility

## CLI Integration

The CLI may expose version-aware operations, but RFC-0004 remains independent
from CLI implementation.

## Input

A CLI command may receive:

```text
--version 1.4.2
--constraint ">=1.4.0,<2.0.0"
```

Input SHALL be delegated to canonical parsing logic.

The CLI SHALL NOT implement its own semantic-version parser.

## Errors

Invalid versions or constraints SHOULD be surfaced as deterministic interface
errors.

The underlying cause remains a domain validation error.

## Output

CLI output MAY display:

- requested constraint;
- selected version;
- incompatible candidates;
- diagnostic explanations.

Formatting belongs to the interface and diagnostic layers.

## Separation

```text
CLI
 |
 v
Application / Resolver
 |
 v
RFC-0004 Domain Semantics
```

Typer, terminal coloring, and rendering SHALL NOT become dependencies of the
versioning model.
