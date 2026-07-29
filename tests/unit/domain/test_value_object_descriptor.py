from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)
from familyos_cli.domain.models.value_object_descriptor import (
    ValueObjectDescriptor,
)


def test_value_object_descriptor_supports_attribute_descriptors() -> None:
    value_object = ValueObjectDescriptor(
        name="EmailAddress",
        description="Email value object",
        attributes=[
            AttributeDescriptor(
                name="value",
                type="str",
                required=True,
            ),
        ],
    )

    assert value_object.name == "EmailAddress"

    assert len(value_object.attributes) == 1

    assert value_object.attributes[0].name == "value"

    assert value_object.attributes[0].type == "str"

    assert value_object.attributes[0].required is True
