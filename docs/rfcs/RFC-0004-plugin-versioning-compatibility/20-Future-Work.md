# RFC-0004 — Plugin Versioning & Compatibility

## Future Work

Future evolution may include:

- disjunctive constraints;
- wildcard constraints;
- lockfiles;
- reproducible resolution snapshots;
- richer pre-release policies;
- API-contract version dimensions;
- compatibility deprecation metadata;
- upgrade recommendation metadata;
- registry-side compatibility indexing;
- property-based testing of ordering and range boundaries;
- formal compatibility conformance suites;
- migration tooling for constraint syntax.

## Evolution Rule

A new compatibility feature SHALL NOT be introduced only in the resolver or
CLI.

It must first define:

1. textual syntax;
2. domain representation;
3. evaluation semantics;
4. backward compatibility;
5. diagnostics;
6. migration behavior;
7. tests.

This protects the ecosystem from semantic drift as the plugin platform grows.
