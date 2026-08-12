# RFC-0004 — Plugin Versioning & Compatibility

## Version Constraints

A version constraint is an explicit predicate over a candidate version.

## Exact Equality

```text
==1.2.3
```

Satisfied only when the candidate has equal semantic precedence.

## Ordered Comparisons

```text
>1.2.3
>=1.2.3
<2.0.0
<=2.0.0
```

These use `PluginVersion` ordering.

## Caret Compatibility

```text
^2.3.4
```

means:

```text
candidate >= 2.3.4
candidate < 3.0.0
```

For zero-major versions:

```text
^0.3.4 -> >=0.3.4,<0.4.0
^0.0.4 -> >=0.0.4,<0.0.5
```

## Tilde Compatibility

```text
~2.3.4
```

means:

```text
candidate >= 2.3.4
candidate < 2.4.0
```

## Compound Constraints

Textual constraint sets are comma-separated:

```text
>=1.2.0,<2.0.0
```

Whitespace around atomic expressions may be normalized.

The set uses logical AND semantics.

## Invalid Expressions

Unsupported operators, missing reference versions, invalid version strings,
and empty sets SHALL be rejected.
