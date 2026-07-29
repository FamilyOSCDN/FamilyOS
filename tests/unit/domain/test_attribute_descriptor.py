from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)


def test_attribute_descriptor_creation() -> None:
    attribute = AttributeDescriptor(
        name="first_name",
        type="str",
        required=True,
        description="Person first name",
    )

    assert attribute.name == "first_name"

    assert attribute.type == "str"

    assert attribute.required is True

    assert attribute.description == "Person first name"
