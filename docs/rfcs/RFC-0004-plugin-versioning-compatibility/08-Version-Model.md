# RFC-0004 — Plugin Versioning & Compatibility

## Version Model

## Canonical Syntax

```text
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

Examples:

```text
0.1.0
1.0.0
1.2.3-alpha
1.2.3-alpha.1
1.2.3-rc.2+build.45
```

## Major, Minor, Patch

Core components are non-negative integers.

Core precedence compares the tuple:

```text
(major, minor, patch)
```

## Pre-release

Pre-release identifiers are dot-separated.

Examples:

```text
alpha
alpha.1
beta.2
rc.1
```

If two versions have identical core components:

- stable > pre-release;
- numeric identifiers compare numerically;
- numeric identifiers have lower precedence than non-numeric identifiers;
- non-numeric identifiers compare lexically;
- if shared identifiers are equal, the longer sequence has higher precedence.

## Build Metadata

Build metadata follows `+`.

Examples:

```text
1.2.3+build.7
1.2.3+sha.abc123
```

Build metadata is preserved by string formatting.

It does not affect precedence or compatibility comparison.

## Canonical Formatting

Parsing and converting back to string SHALL preserve the semantic version
structure in canonical form.
