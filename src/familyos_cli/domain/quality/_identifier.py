def validate_quality_identifier(value: str, *, namespace: str, type_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{type_name} value must be a str")
    prefix = f"{namespace}-"
    if not value.startswith(prefix):
        raise ValueError(f"{type_name} value must start with {prefix}")
    suffix = value[len(prefix) :]
    if not suffix:
        raise ValueError(f"{type_name} value must contain a non-empty suffix")
    if value != value.strip() or any(c.isspace() for c in suffix):
        raise ValueError(f"{type_name} value must be canonical")
