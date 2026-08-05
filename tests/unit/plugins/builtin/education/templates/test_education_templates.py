from pathlib import Path

TEMPLATE_ROOT = (
    Path(__file__)
    .parents[6]
    / "src"
    / "familyos_cli"
    / "plugins"
    / "builtin"
    / "education"
    / "templates"
)


def test_education_templates_exist() -> None:
    templates = [
        (
            "domain",
            "education_domain.md.j2",
        ),
        (
            "validation",
            "education_validation.md.j2",
        ),
        (
            "capabilities",
            "education_capabilities.md.j2",
        ),
        (
            "documentation",
            "education_documentation.md.j2",
        ),
    ]

    for directory, filename in templates:
        assert (
            TEMPLATE_ROOT
            / directory
            / filename
        ).exists()
