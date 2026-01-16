#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class JavaJar(AutomationTool):
    name = "java_jar"
    module = "command"
    description = "Run a java jar"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, jar: str, args: list):
        """Run a java jar

        Args:
            jar: the path of the jar file
            args: other arguments to the jar

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            self.context.gate_cache,
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"java -jar {jar} {' '.join(args)}",
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output