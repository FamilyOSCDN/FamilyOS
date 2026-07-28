"""Template context."""

from datetime import datetime


class TemplateContext:
    """Provide global template variables."""

    def build(
        self,
        context: dict[str, object],
    ) -> dict[str, object]:
        """Return the complete rendering context."""

        return {
            "year": datetime.now().year,
            "generator": "FamilyOS CLI",
            "version": "0.1.0",
            **context,
        }
