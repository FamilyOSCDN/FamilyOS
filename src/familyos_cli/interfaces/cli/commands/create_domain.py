"""Create domain command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.generation.domain_generation_adapter import (
    DomainGenerationAdapter,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.domain.generation.artifact_generation_mapper import (
    ArtifactGenerationMapper,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.interfaces.cli.error_handler import ErrorHandler
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


def create_domain(
    name: Annotated[
        str,
        typer.Argument(
            ...,
            help="Domain name.",
        ),
    ],
    destination: Annotated[
        Path | None,
        typer.Option(
            "--destination",
            "-d",
            help="Generation destination.",
        ),
    ] = None,
) -> None:
    """Create a FamilyOS domain."""

    target = destination or Path(".")

    try:
        specification = DomainSpecification(
            name=name,
            entities=[],
            aggregates=[],
            repositories=[],
            services=[],
        )

        pipeline = DomainGenerationPipeline(
            planner=DomainGenerationPlanner(),
            mapper=ArtifactGenerationMapper(),
            adapter=DomainGenerationAdapter(),
            engine=GenerationEngine(),
        )

        pipeline.generate(
            specification=specification,
            destination=target,
        )

        Output.success(
            f'Domain "{name}" created successfully.',
        )

    except FamilyOSError as error:
        ErrorHandler.handle(error)