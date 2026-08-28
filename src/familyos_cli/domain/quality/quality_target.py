from dataclasses import dataclass


def _required(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"QualityTarget {name} must be a str")
    if not value:
        raise ValueError(f"QualityTarget {name} must be non-empty")


@dataclass(frozen=True, slots=True)
class QualityTarget:
    target_type: str
    identifier: str
    revision: str | None = None
    version: str | None = None
    path: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        _required(self.target_type, "target_type")
        _required(self.identifier, "identifier")
        for n in ("revision", "version", "path"):
            v = getattr(self, n)
            if v is not None:
                _required(v, n)
        if not isinstance(self.metadata, tuple):
            raise TypeError("QualityTarget metadata must be a tuple")
        for e in self.metadata:
            if not isinstance(e, tuple) or len(e) != 2:
                raise TypeError(
                    "QualityTarget metadata entries must be (str, str) tuples"
                )
            k, v = e
            if not isinstance(k, str) or not isinstance(v, str):
                raise TypeError(
                    "QualityTarget metadata entries must contain str values"
                )
            if not k:
                raise ValueError("QualityTarget metadata keys must be non-empty")
            if not v:
                raise ValueError("QualityTarget metadata values must be non-empty")
