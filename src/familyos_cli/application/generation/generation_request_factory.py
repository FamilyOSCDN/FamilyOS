"""Generation request factory."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


class GenerationRequestFactory:
    """Create generation requests."""

    def create(
        self,
        domain_name: str,
        recipe_name: str = "domain_documentation",
    ) -> GenerationRequest:
        """Create a generation request."""

        return GenerationRequest(
            domain_name=domain_name,
            recipe_name=recipe_name,
        )
