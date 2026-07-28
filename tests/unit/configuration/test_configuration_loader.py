from pathlib import Path

from familyos_cli.configuration.loader import ConfigurationLoader


def test_configuration_loader_loads_yaml(tmp_path: Path) -> None:
    config_file = tmp_path / "familyos.yml"

    config_file.write_text(
        """
project:
  name: FamilyOS
  version: "1.0"
  description: Test project
  author: Thierry

plugins:
  - sample-plugin
""",
        encoding="utf-8",
    )

    loader = ConfigurationLoader()

    config = loader.load(config_file)

    assert config.project.name == "FamilyOS"
    assert config.project.version == "1.0"
    assert config.plugins == ["sample-plugin"]
