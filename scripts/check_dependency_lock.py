"""Verify the generated dependency state without modifying it."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from re import MULTILINE, search
from shutil import copyfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.compile_dependencies import (
        DEPENDENCY_DIGEST_PREFIX,
        LOCK_PATH,
        compile_dependencies,
        dependency_input_digest,
    )
elif __package__:
    from .compile_dependencies import (
        DEPENDENCY_DIGEST_PREFIX,
        LOCK_PATH,
        compile_dependencies,
        dependency_input_digest,
    )
else:
    from compile_dependencies import (
        DEPENDENCY_DIGEST_PREFIX,
        LOCK_PATH,
        compile_dependencies,
        dependency_input_digest,
    )


class DependencyInputDriftError(RuntimeError):
    """Canonical dependency declarations differ from the tracked digest."""


class ResolvedLockDriftError(RuntimeError):
    """Seeded resolution differs from the tracked lock."""


def check_dependency_lock(lock_path: Path = LOCK_PATH) -> None:
    """Require canonical inputs and seeded resolution to match the tracked lock."""

    tracked_content = lock_path.read_text(encoding="utf-8")
    digest_match = search(
        rf"^{DEPENDENCY_DIGEST_PREFIX}([0-9a-f]{{64}})$",
        tracked_content,
        flags=MULTILINE,
    )
    current_digest = dependency_input_digest()
    if digest_match is None or digest_match.group(1) != current_digest:
        raise DependencyInputDriftError(
            "canonical dependency inputs changed; regenerate requirements.txt.",
        )

    with tempfile.TemporaryDirectory(prefix="familyos-dependency-lock-") as directory:
        generated_path = Path(directory) / "requirements.txt"
        copyfile(lock_path, generated_path)
        compile_dependencies(generated_path)
        if lock_path.read_bytes() != generated_path.read_bytes():
            raise ResolvedLockDriftError(
                "resolved lock content changed; regenerate requirements.txt.",
            )


def main() -> int:
    """Check lock freshness and provide an actionable failure."""

    try:
        check_dependency_lock()
    except DependencyInputDriftError as error:
        print(f"Dependency lock input drift: {error}", file=sys.stderr)
        return 1
    except ResolvedLockDriftError as error:
        print(f"Dependency lock resolution drift: {error}", file=sys.stderr)
        return 1
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Dependency lock check failed: {error}", file=sys.stderr)
        return 1

    print("requirements.txt is synchronized with pyproject.toml.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
