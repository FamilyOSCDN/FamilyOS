from familyos_cli.plugins.builtin.education.capabilities.education_record_capability import (
    EducationRecordCapability,
)


def test_education_record_capability_creation() -> None:
    capability = (
        EducationRecordCapability.create()
    )

    assert str(capability.id) == (
        "familyos.education.record"
    )

    assert capability.display_name == (
        "Education Record"
    )

    assert (
        "educational record"
        in capability.description
    )
