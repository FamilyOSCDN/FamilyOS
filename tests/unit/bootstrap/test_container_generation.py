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
