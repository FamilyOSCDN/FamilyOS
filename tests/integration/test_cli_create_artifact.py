from __future__ import annotations

from pathlib import Path

from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)


def test_should_create_artifact(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    specifications = tmp_path / "specifications"
    specifications.mkdir()

    (
        specifications / "registry.yaml"
    ).write_text(
        """
version: 1

artifacts:
  - id: domain
    specification: domain/domain.yaml
""",
        encoding="utf-8",
    )

    domain_specification = specifications / "domain"
    domain_specification.mkdir()

    (
        domain_specification / "domain.yaml"
    ).write_text(
        """
project:
  name: domain
  directories: []
  files: []
""",
        encoding="utf-8",
    )

    templates = tmp_path / "templates" / "domain"
    templates.mkdir(parents=True)

    (
        templates / "manifest.yml.j2"
    ).write_text(
        "type: {{ artifact_type }}\nname: {{ name }}\n",
        encoding="utf-8",
    )

    use_case = CreateArtifactUseCase()

    use_case.execute(
        artifact_type="domain",
        name="Person",
    )