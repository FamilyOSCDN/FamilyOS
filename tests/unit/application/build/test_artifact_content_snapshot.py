from __future__ import annotations

import pytest

from familyos_cli.application.build.artifact_content_snapshot import (
    ArtifactContentMember,
    ArtifactContentSnapshot,
)
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
)
from familyos_cli.application.build.artifact_type import ArtifactClass

_DIGEST_A = "a" * 64
_DIGEST_B = "b" * 64


def _member(
    path: str = "familyos_cli/__init__.py",
    *,
    size: int = 10,
    digest: str = _DIGEST_A,
) -> ArtifactContentMember:
    return ArtifactContentMember(
        path=path,
        size=size,
        digest_algorithm=ArtifactDigestAlgorithm.SHA256,
        digest=digest,
    )


def test_content_member_preserves_canonical_identity() -> None:
    member = _member()

    assert member.path == "familyos_cli/__init__.py"
    assert member.size == 10
    assert member.digest_algorithm is ArtifactDigestAlgorithm.SHA256
    assert member.digest == _DIGEST_A


@pytest.mark.parametrize(
    "path",
    (
        "",
        "/absolute.py",
        "../escape.py",
        "pkg/../escape.py",
        "pkg/./module.py",
        "pkg//module.py",
        r"pkg\module.py",
        "C:/module.py",
    ),
)
def test_content_member_rejects_noncanonical_path(path: str) -> None:
    with pytest.raises(ValueError):
        _member(path)


def test_content_member_rejects_negative_size() -> None:
    with pytest.raises(ValueError):
        _member(size=-1)


@pytest.mark.parametrize(
    "digest",
    (
        "",
        "a" * 63,
        "a" * 65,
        "A" * 64,
        "g" * 64,
    ),
)
def test_content_member_rejects_noncanonical_sha256(digest: str) -> None:
    with pytest.raises(ValueError):
        _member(digest=digest)


def test_snapshot_preserves_sorted_members() -> None:
    first = _member("a.py", digest=_DIGEST_A)
    second = _member("b.py", digest=_DIGEST_B)

    snapshot = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(first, second),
    )

    assert snapshot.members == (first, second)


def test_snapshot_rejects_unsorted_members() -> None:
    first = _member("a.py", digest=_DIGEST_A)
    second = _member("b.py", digest=_DIGEST_B)

    with pytest.raises(ValueError):
        ArtifactContentSnapshot(
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            members=(second, first),
        )


def test_snapshot_rejects_duplicate_member_paths() -> None:
    first = _member("same.py", digest=_DIGEST_A)
    second = _member("same.py", digest=_DIGEST_B)

    with pytest.raises(ValueError):
        ArtifactContentSnapshot(
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            members=(first, second),
        )


def test_equivalent_snapshots_match() -> None:
    member = _member()

    first = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(member,),
    )
    second = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(member,),
    )

    assert first.matches(second)
    assert second.matches(first)


def test_changed_member_content_does_not_match() -> None:
    first = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(_member(digest=_DIGEST_A),),
    )
    second = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(_member(digest=_DIGEST_B),),
    )

    assert not first.matches(second)


def test_different_artifact_types_do_not_match() -> None:
    member = _member()

    wheel = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        members=(member,),
    )
    sdist = ArtifactContentSnapshot(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        members=(member,),
    )

    assert not wheel.matches(sdist)
