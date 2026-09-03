"""Atomic file output at the Quality CLI boundary."""

from pathlib import Path
from tempfile import NamedTemporaryFile


def write_quality_report(path: Path, rendered: str) -> None:
    """Replace a destination only after a complete UTF-8 sibling write."""
    encoded = rendered.encode("utf-8")
    temporary: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="wb", dir=path.parent, prefix=f".{path.name}.",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(encoded)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
