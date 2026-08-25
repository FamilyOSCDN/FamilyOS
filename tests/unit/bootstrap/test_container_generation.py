from pathlib import Path

from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
)
from familyos_cli.bootstrap.container import (
    ApplicationContainer,
)


def test_container_creates_domain_generation_use_case() -> None:
    container = ApplicationContainer()

    use_case = container.create_domain_use_case()

    assert isinstance(
        use_case,
        CreateDomainUseCase,
    )


def test_application_container_preserves_explicit_project_root(
    tmp_path: Path,
) -> None:
    """Composition root preserves an explicitly selected repository root."""
    container = ApplicationContainer(project_root=tmp_path)

    assert container.project_root == tmp_path.resolve()
