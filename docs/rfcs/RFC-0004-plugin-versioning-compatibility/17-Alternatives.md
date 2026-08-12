# RFC-0004 — Plugin Versioning & Compatibility

## Alternatives

## Alternative A — Lexical Version Comparison

Rejected.

Lexical ordering does not provide semantic version precedence.

## Alternative B — Exact Versions Only

Rejected.

Exact-only dependencies would force unnecessary coordination between plugin
release schedules and would prevent compatible-range declarations.

## Alternative C — Resolver-Owned Semantics

Rejected.

Embedding compatibility rules inside graph resolution makes those rules
difficult to reuse and test independently.

## Alternative D — Repository-Owned Semantics

Rejected.

Compatibility must be identical regardless of package source.

## Alternative E — Permissive Parsing

Rejected.

Silently coercing malformed versions or unsupported operators creates
non-deterministic behavior and hides configuration errors.

## Alternative F — OR Semantics for Comma-Separated Constraints

Rejected for the canonical syntax.

Comma-separated constraints are conjunctive.

If disjunction is required later, it must receive explicit syntax and
governance.

## Alternative G — Build Metadata Affects Precedence

Rejected.

Build metadata is intentionally excluded from semantic precedence.
