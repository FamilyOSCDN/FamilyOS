# RFC-0004 — Plugin Versioning & Compatibility

## Migration

RFC-0004 replaces the historical placeholder identifier `RFC-000AA`.

The historical RFC directory contained a documentation skeleton rather than a
complete normative specification.

## Migration Goals

- establish `RFC-0004` as the canonical identifier;
- replace active references to `RFC-000AA`;
- reconstruct normative documentation from the implemented architecture;
- preserve existing compatibility behavior;
- avoid introducing undocumented runtime changes.

## Compatibility

The identifier migration SHALL NOT alter plugin version semantics.

Existing valid plugin manifests and dependency declarations remain governed by
the same implementation behavior.

## Historical References

A historical mention of `RFC-000AA` MAY remain when explicitly identified as
history.

It SHALL NOT remain as an active architectural dependency.

## Validation

Migration is complete when:

- no active `RFC-000AA` references remain;
- all RFC-0004 documents are canonical;
- draft placeholders are removed;
- version and constraint tests pass;
- repository quality gates pass.
