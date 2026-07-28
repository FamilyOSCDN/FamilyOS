from unittest.mock import patch

from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)


def test_should_create_domain_artifact() -> None:
    use_case = CreateArtifactUseCase()

    with patch.object(
        use_case._domain_generator,
        "generate",
    ) as mock_generate:
        use_case.execute(
            artifact_type="domain",
            name="Person",
        )

    mock_generate.assert_called_once()


def test_should_create_generic_artifact() -> None:
    use_case = CreateArtifactUseCase()

    with patch.object(
        use_case.generator,
        "generate",
    ) as mock_generate:
        use_case.execute(
            artifact_type="plugin",
            name="MyPlugin",
        )

    mock_generate.assert_called_once_with(
        artifact_type="plugin",
        name="MyPlugin",
    )
