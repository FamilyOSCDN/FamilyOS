from familyos_cli.application.use_cases.check_plugin_compliance import (
    CheckPluginComplianceUseCase,
)
from familyos_cli.bootstrap.container import ApplicationContainer


def test_container_creates_check_plugin_compliance_use_case() -> None:
    container = ApplicationContainer()

    use_case = container.check_plugin_compliance_use_case()

    assert isinstance(
        use_case,
        CheckPluginComplianceUseCase,
    )
