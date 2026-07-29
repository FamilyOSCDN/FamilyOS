from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)


def test_entity_descriptor_supports_attribute_descriptors() -> None:
    entity = EntityDescriptor(
        name="Person",
        description="Person entity",
        attributes=[
            AttributeDescriptor(
                name="first_name",
                type="str",
                required=True,
            ),
        ],
        behaviors=[
            "update_profile",
        ],
        business_rules=[
            "Person must have a unique identifier",
        ],
        relationships=[
            "Person belongs to Family",
        ],
    )

    assert entity.name == "Person"

    assert len(entity.attributes) == 1

    assert entity.attributes[0].name == "first_name"

    assert entity.attributes[0].type == "str"

    assert entity.attributes[0].required is True

    assert entity.behaviors == [
        "update_profile",
    ]

    assert entity.business_rules == [
        "Person must have a unique identifier",
    ]

    assert entity.relationships == [
        "Person belongs to Family",
    ]
