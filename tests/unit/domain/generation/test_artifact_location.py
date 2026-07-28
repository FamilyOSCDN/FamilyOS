from familyos_cli.domain.generation.artifact_location import (
    ArtifactLocation,
)


def test_should_expose_expected_artifact_locations() -> None:
    assert ArtifactLocation.DOMAIN.value == "domain"
    assert ArtifactLocation.APPLICATION.value == "application"
    assert ArtifactLocation.INFRASTRUCTURE.value == "infrastructure"
    assert ArtifactLocation.INTERFACES.value == "interfaces"
    assert ArtifactLocation.TESTS.value == "tests"
    assert ArtifactLocation.DOCUMENTATION.value == "documentation"