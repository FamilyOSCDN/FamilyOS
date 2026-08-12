# RFC-0004 — Plugin Versioning & Compatibility

## Open Questions

The accepted RFC-0004 baseline is intentionally small.

The following topics remain candidates for future RFCs or revisions.

### Disjunction

Should FamilyOS support expressions such as:

```text
^1.0.0 OR ^2.0.0
```

No syntax is currently canonical.

### Wildcards

Should expressions such as `1.4.*` or `1.x` be supported?

### Lockfiles

Should dependency resolution produce a lockfile or reproducible resolution
snapshot?

### Pre-release Policy

Should manifests be able to explicitly opt into or exclude pre-release
candidates beyond ordinary precedence behavior?

### API Compatibility

Should future compatibility include a separate plugin API-contract version in
addition to package version?

### Deprecation Metadata

Should dependencies express deprecation windows or preferred upgrade targets?

### Resolver Preference

Should candidate preference be configurable when several compatible versions
exist?

None of these questions changes the accepted baseline implicitly.

Each new capability must define parsing, semantics, migration, diagnostics, and
test coverage before adoption.
