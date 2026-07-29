from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)
from familyos_cli.domain.models.project_file import (
    ProjectFile,
)
from familyos_cli.domain.models.value_object_descriptor import (
    ValueObjectDescriptor,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)


def test_file_generator_should_render_value_object_template(
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
                path="value_objects/email_address.py",
                template="value_object.py.jinja",
            ),
        ],
        context={
            "value_object": ValueObjectDescriptor(
                name="EmailAddress",
                description="Email address value object",
                attributes=[
                    AttributeDescriptor(
                        name="value",
                        type="str",
                        required=True,
                    ),
                ],
            ),
        },
    )

    generated_file = (
        destination
        / "value_objects/email_address.py"
    )

    content = generated_file.read_text(
        encoding="utf-8",
    )

    assert "class EmailAddress:" in content

    assert "self.value = None" in content
