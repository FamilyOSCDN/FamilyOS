"""Tests for canonical Build failure categories."""

from familyos_cli.application.build.build_failure_category import (
    BuildFailureCategory,
)


def test_build_failure_categories_are_stable() -> None:
    assert tuple(BuildFailureCategory) == (
        BuildFailureCategory.INPUT,
        BuildFailureCategory.CONFIGURATION,
        BuildFailureCategory.DEPENDENCY,
        BuildFailureCategory.TOOLCHAIN,
        BuildFailureCategory.ENVIRONMENT,
        BuildFailureCategory.EXECUTION,
        BuildFailureCategory.ARTIFACT,
        BuildFailureCategory.VALIDATION,
        BuildFailureCategory.INTEGRITY,
    )


def test_build_failure_category_values_are_machine_readable() -> None:
    assert {
        category.value for category in BuildFailureCategory
    } == {
        "input",
        "configuration",
        "dependency",
        "toolchain",
        "environment",
        "execution",
        "artifact",
        "validation",
        "integrity",
    }


def test_validation_domains_have_complete_failure_category_mapping() -> None:
    from familyos_cli.application.build.build_validation import (
        BuildValidationDomain,
    )

    expected = {
        BuildValidationDomain.INPUT: BuildFailureCategory.INPUT,
        BuildValidationDomain.SOURCE: BuildFailureCategory.INPUT,
        BuildValidationDomain.CONFIGURATION: (
            BuildFailureCategory.CONFIGURATION
        ),
        BuildValidationDomain.DEPENDENCY: BuildFailureCategory.DEPENDENCY,
        BuildValidationDomain.TOOLCHAIN: BuildFailureCategory.TOOLCHAIN,
        BuildValidationDomain.ENVIRONMENT: BuildFailureCategory.ENVIRONMENT,
        BuildValidationDomain.TESTING: BuildFailureCategory.VALIDATION,
        BuildValidationDomain.COMPLIANCE: BuildFailureCategory.VALIDATION,
        BuildValidationDomain.EXECUTION: BuildFailureCategory.EXECUTION,
        BuildValidationDomain.ARTIFACT: BuildFailureCategory.ARTIFACT,
        BuildValidationDomain.METADATA: BuildFailureCategory.ARTIFACT,
        BuildValidationDomain.INTEGRITY: BuildFailureCategory.INTEGRITY,
        BuildValidationDomain.FUNCTIONAL_ARTIFACT: (
            BuildFailureCategory.ARTIFACT
        ),
        BuildValidationDomain.EVIDENCE: BuildFailureCategory.VALIDATION,
    }

    assert set(expected) == set(BuildValidationDomain)

    from familyos_cli.application.build.build_failure_category import (
        failure_category_for_validation_domain,
    )

    for domain, category in expected.items():
        assert failure_category_for_validation_domain(domain) is category


def test_source_failure_is_classified_as_build_input_failure() -> None:
    from familyos_cli.application.build.build_failure_category import (
        failure_category_for_validation_domain,
    )
    from familyos_cli.application.build.build_validation import (
        BuildValidationDomain,
    )

    assert (
        failure_category_for_validation_domain(BuildValidationDomain.SOURCE)
        is BuildFailureCategory.INPUT
    )


def test_specialized_validation_domains_remain_validation_failures() -> None:
    from familyos_cli.application.build.build_failure_category import (
        failure_category_for_validation_domain,
    )
    from familyos_cli.application.build.build_validation import (
        BuildValidationDomain,
    )

    for domain in (
        BuildValidationDomain.TESTING,
        BuildValidationDomain.COMPLIANCE,
        BuildValidationDomain.EVIDENCE,
    ):
        assert (
            failure_category_for_validation_domain(domain)
            is BuildFailureCategory.VALIDATION
        )


def test_artifact_related_domains_share_artifact_failure_category() -> None:
    from familyos_cli.application.build.build_failure_category import (
        failure_category_for_validation_domain,
    )
    from familyos_cli.application.build.build_validation import (
        BuildValidationDomain,
    )

    for domain in (
        BuildValidationDomain.ARTIFACT,
        BuildValidationDomain.METADATA,
        BuildValidationDomain.FUNCTIONAL_ARTIFACT,
    ):
        assert (
            failure_category_for_validation_domain(domain)
            is BuildFailureCategory.ARTIFACT
        )


def test_execution_stages_have_complete_failure_category_mapping() -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionStage,
    )
    from familyos_cli.application.build.build_failure_category import (
        failure_category_for_execution_stage,
    )

    expected = {
        BuildExecutionStage.VALIDATE_INPUTS: BuildFailureCategory.INPUT,
        BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT: (
            BuildFailureCategory.INPUT
        ),
        BuildExecutionStage.VALIDATE_TOOLCHAIN: BuildFailureCategory.TOOLCHAIN,
        BuildExecutionStage.VALIDATE_ENVIRONMENT: (
            BuildFailureCategory.ENVIRONMENT
        ),
        BuildExecutionStage.INITIALIZE_WORKSPACE: (
            BuildFailureCategory.ENVIRONMENT
        ),
        BuildExecutionStage.RESOLVE_BUILD_CONTEXT: (
            BuildFailureCategory.CONFIGURATION
        ),
        BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION: (
            BuildFailureCategory.CONFIGURATION
        ),
        BuildExecutionStage.STAGE_BUILD_INPUTS: BuildFailureCategory.INPUT,
        BuildExecutionStage.PACKAGE: BuildFailureCategory.EXECUTION,
        BuildExecutionStage.DISCOVER_ARTIFACTS: BuildFailureCategory.ARTIFACT,
        BuildExecutionStage.VALIDATE_ARTIFACTS: BuildFailureCategory.ARTIFACT,
        BuildExecutionStage.ESTABLISH_ARTIFACT_IDENTITY: (
            BuildFailureCategory.ARTIFACT
        ),
        BuildExecutionStage.ESTABLISH_ARTIFACT_INTEGRITY: (
            BuildFailureCategory.INTEGRITY
        ),
        BuildExecutionStage.BUILD_ARTIFACT_MANIFEST: (
            BuildFailureCategory.ARTIFACT
        ),
        BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL: (
            BuildFailureCategory.ARTIFACT
        ),
        BuildExecutionStage.FINALIZE_EXECUTION: (
            BuildFailureCategory.EXECUTION
        ),
    }

    assert set(expected) == set(BuildExecutionStage)

    for stage, category in expected.items():
        assert failure_category_for_execution_stage(stage) is category


def test_each_failure_category_has_corrective_information() -> None:
    from familyos_cli.application.build.build_failure_category import (
        corrective_information_for_failure_category,
    )

    for category in BuildFailureCategory:
        corrective_information = (
            corrective_information_for_failure_category(category)
        )

        assert corrective_information
        assert corrective_information.strip() == corrective_information


def test_corrective_information_is_stable_and_category_specific() -> None:
    from familyos_cli.application.build.build_failure_category import (
        corrective_information_for_failure_category,
    )

    expected = {
        BuildFailureCategory.INPUT:
            "Correct the invalid build input and retry.",
        BuildFailureCategory.CONFIGURATION:
            "Correct the effective build configuration and retry.",
        BuildFailureCategory.DEPENDENCY:
            "Restore the required dependency state and retry.",
        BuildFailureCategory.TOOLCHAIN:
            "Restore the required build toolchain and retry.",
        BuildFailureCategory.ENVIRONMENT:
            "Correct the build environment and retry.",
        BuildFailureCategory.EXECUTION:
            "Correct the failed build execution condition and retry.",
        BuildFailureCategory.ARTIFACT:
            "Correct the generated artifact and retry the build.",
        BuildFailureCategory.VALIDATION:
            "Correct the failed validation requirement and retry.",
        BuildFailureCategory.INTEGRITY:
            "Restore artifact integrity before continuing.",
    }

    assert {
        category: corrective_information_for_failure_category(category)
        for category in BuildFailureCategory
    } == expected
