from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_education_plugin_registers_capabilities_in_runtime() -> None:
    runtime = PluginRuntime()

    runtime.activate(
        EducationPlugin(),
    )

    capabilities = (
        runtime.capabilities()
        .list()
    )

    identifiers = {
        str(capability.id)
        for capability in capabilities
    }

    assert (
        "familyos.education.learner"
        in identifiers
    )

    assert (
        "familyos.education.course"
        in identifiers
    )

    assert (
        "familyos.education.record"
        in identifiers
    )
