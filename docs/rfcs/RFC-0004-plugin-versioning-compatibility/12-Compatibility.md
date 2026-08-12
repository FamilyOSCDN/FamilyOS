# RFC-0004 — Plugin Versioning & Compatibility

## Compatibility

Compatibility is the result of applying a constraint or constraint set to a
candidate `PluginVersion`.

## Direct Comparison Semantics

```text
==  equal precedence
>   greater precedence
>=  greater or equal precedence
<   lower precedence
<=  lower or equal precedence
```

## Caret Semantics

Caret defines a bounded range.

If major > 0:

```text
^M.m.p -> >=M.m.p, <(M+1).0.0
```

If major == 0 and minor > 0:

```text
^0.m.p -> >=0.m.p, <0.(m+1).0
```

If major == 0 and minor == 0:

```text
^0.0.p -> >=0.0.p, <0.0.(p+1)
```

## Tilde Semantics

```text
~M.m.p -> >=M.m.p, <M.(m+1).0
```

## Compound Semantics

For:

```text
>=1.4.0,<2.0.0
```

both comparisons must succeed.

## No Implicit Compatibility

Compatibility SHALL NOT be inferred from:

- plugin names;
- package filenames;
- repository priority;
- discovery order;
- installation order;
- runtime state.

Only explicit version values and explicit constraints determine RFC-0004
compatibility.
