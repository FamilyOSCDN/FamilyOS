from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)
from familyos_cli.domain.models.project_file import (
    ProjectFile,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)


def test_file_generator_should_render_entity_template(
    tmp_path: Path,
) -> None:
    template_directory = (
        Path(__file__)
        .parents[4]
        / "templates"
    )

    generator = FileGenerator(
        template_directories=(
            template_directory,
        ),
    )

    destination = tmp_path / "output"

    generator.generate(
        destination=destination,
        files=[
            ProjectFile(
                path="models/person.py",
                template="entity.py.jinja",
            ),
        ],
        context={
            "entity": EntityDescriptor(
                name="Person",
                description="Human identity entity",
                attributes=[
                    AttributeDescriptor(
                        name="first_name",
                        type="str",
                        required=True,
                    ),
                    AttributeDescriptor(
                        name="last_name",
                        type="str",
                    ),
                ],
            ),
        },
    )

    generated_file = destination / "models/person.py"

    content = generated_file.read_text(
        encoding="utf-8",
    )

    assert "class Person:" in content

    assert "self.first_name = None" in content

    assert "self.last_name = None" in content
