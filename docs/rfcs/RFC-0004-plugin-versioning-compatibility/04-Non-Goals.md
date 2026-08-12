# RFC-0004 — Plugin Versioning & Compatibility

## Non-Goals

RFC-0004 deliberately does not own every part of plugin resolution.

It does not define:

- plugin discovery;
- package repository protocols;
- remote registry communication;
- package download;
- installation transactions;
- dependency graph traversal;
- cycle detection;
- graph-level conflict resolution;
- diagnostic formatting;
- terminal rendering;
- CLI exit codes;
- plugin activation;
- plugin runtime lifecycle;
- plugin trust or sandboxing;
- cryptographic signing;
- automatic dependency repair;
- marketplace behavior.

RFC-0004 also does not define a second plugin identity model.

Plugin identifiers remain governed by the applicable FamilyOS identity
contracts.

The RFC defines version and compatibility semantics only.

Higher-level policies may consume these semantics but SHALL NOT be folded into
the versioning domain merely for convenience.
