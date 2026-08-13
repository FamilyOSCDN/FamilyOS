"""Default compliance validator registry factory."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.validator_registry import (
    ValidatorRegistry,
)
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_import_boundary_validator import (
    VALIDATOR_ID as ARCHITECTURE_IMPORT_BOUNDARY_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_import_boundary_validator import (
    ArchitectureImportBoundaryValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_no_wildcard_imports_validator import (
    VALIDATOR_ID as ARCHITECTURE_NO_WILDCARD_IMPORTS_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_no_wildcard_imports_validator import (
    ArchitectureNoWildcardImportsValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.capability_namespace_validator import (
    VALIDATOR_ID as CAPABILITY_NAMESPACE_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.capability_namespace_validator import (
    CapabilityNamespaceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.capability_uniqueness_validator import (
    VALIDATOR_ID as CAPABILITY_UNIQUENESS_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.capability_uniqueness_validator import (
    CapabilityUniquenessValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_expression_format_validator import (
    VALIDATOR_ID as DEPENDENCY_EXPRESSION_FORMAT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_expression_format_validator import (
    DependencyExpressionFormatValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_no_self_dependency_validator import (
    VALIDATOR_ID as DEPENDENCY_NO_SELF_DEPENDENCY_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_no_self_dependency_validator import (
    DependencyNoSelfDependencyValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_id_format_validator import (
    VALIDATOR_ID as IDENTITY_ID_FORMAT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_id_format_validator import (
    IdentityIdFormatValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_manifest_presence_validator import (
    VALIDATOR_ID as IDENTITY_MANIFEST_PRESENCE_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_manifest_presence_validator import (
    IdentityManifestPresenceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_namespace_validator import (
    VALIDATOR_ID as IDENTITY_NAMESPACE_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.identity_namespace_validator import (
    IdentityNamespaceValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_consistency_validator import (
    VALIDATOR_ID as METADATA_CONSISTENCY_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_consistency_validator import (
    MetadataConsistencyValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_description_quality_validator import (
    VALIDATOR_ID as METADATA_DESCRIPTION_QUALITY_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_description_quality_validator import (
    MetadataDescriptionQualityValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_name_present_validator import (
    VALIDATOR_ID as METADATA_NAME_PRESENT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_name_present_validator import (
    MetadataNamePresentValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_version_format_validator import (
    VALIDATOR_ID as METADATA_VERSION_FORMAT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.metadata_version_format_validator import (
    MetadataVersionFormatValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_contribution_paths_validator import (
    VALIDATOR_ID as STRUCTURE_CONTRIBUTION_PATHS_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_contribution_paths_validator import (
    StructureContributionPathsValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_entry_point_validator import (
    VALIDATOR_ID as STRUCTURE_ENTRY_POINT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_entry_point_validator import (
    StructureEntryPointValidator,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_package_layout_validator import (
    VALIDATOR_ID as STRUCTURE_PACKAGE_LAYOUT_ID,
)
from familyos_cli.plugins.ecosystem.compliance.validators.structure_package_layout_validator import (
    StructurePackageLayoutValidator,
)


def build_default_validator_registry() -> ValidatorRegistry:
    """Build the default compliance validator registry."""

    registry = ValidatorRegistry()

    registry.register(
        IDENTITY_MANIFEST_PRESENCE_ID,
        IdentityManifestPresenceValidator(),
    )
    registry.register(IDENTITY_ID_FORMAT_ID, IdentityIdFormatValidator())
    registry.register(IDENTITY_NAMESPACE_ID, IdentityNamespaceValidator())

    registry.register(METADATA_NAME_PRESENT_ID, MetadataNamePresentValidator())
    registry.register(
        METADATA_VERSION_FORMAT_ID,
        MetadataVersionFormatValidator(),
    )
    registry.register(
        METADATA_DESCRIPTION_QUALITY_ID,
        MetadataDescriptionQualityValidator(),
    )
    registry.register(METADATA_CONSISTENCY_ID, MetadataConsistencyValidator())

    registry.register(STRUCTURE_ENTRY_POINT_ID, StructureEntryPointValidator())
    registry.register(
        STRUCTURE_PACKAGE_LAYOUT_ID,
        StructurePackageLayoutValidator(),
    )
    registry.register(
        STRUCTURE_CONTRIBUTION_PATHS_ID,
        StructureContributionPathsValidator(),
    )

    registry.register(
        ARCHITECTURE_IMPORT_BOUNDARY_ID,
        ArchitectureImportBoundaryValidator(),
    )
    registry.register(
        ARCHITECTURE_NO_WILDCARD_IMPORTS_ID,
        ArchitectureNoWildcardImportsValidator(),
    )

    registry.register(CAPABILITY_NAMESPACE_ID, CapabilityNamespaceValidator())
    registry.register(CAPABILITY_UNIQUENESS_ID, CapabilityUniquenessValidator())

    registry.register(
        DEPENDENCY_EXPRESSION_FORMAT_ID,
        DependencyExpressionFormatValidator(),
    )
    registry.register(
        DEPENDENCY_NO_SELF_DEPENDENCY_ID,
        DependencyNoSelfDependencyValidator(),
    )

    return registry
