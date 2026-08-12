# RFC-0004 — Plugin Versioning & Compatibility

## Resolution Algorithm

RFC-0004 defines compatibility evaluation, not the full dependency graph
algorithm.

## Atomic Evaluation

Conceptually:

```text
match(constraint, candidate_version)
```

The operation dispatches according to the constraint operator.

## Compound Evaluation

For a constraint set:

```text
matches = all(
    constraint.is_satisfied_by(candidate_version)
    for constraint in constraint_set
)
```

## Candidate Filtering

A higher-level package selector may use RFC-0004 as follows:

```text
compatible = [
    package
    for package in candidates
    if constraints.is_satisfied_by(package.version)
]
```

RFC-0005 may then choose among compatible candidates.

## Example

Constraint:

```text
>=1.4.0,<2.0.0
```

Candidates:

```text
1.3.9 -> false
1.4.0 -> true
1.8.2 -> true
2.0.0 -> false
```

## Invalid Candidate Versions

Invalid semantic version strings SHALL not be granted arbitrary precedence.

A package selector may ignore or report invalid candidates according to the
higher-level resolution contract, but RFC-0004 defines them as invalid
versions.

## Deterministic Property

Equivalent inputs SHALL produce equivalent results regardless of package
discovery order or repository source.
