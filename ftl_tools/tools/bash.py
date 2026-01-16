#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Bash(AutomationTool):
    name = "bash"
    module = "command"
    description = "Run a bash script"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, script: str, user: str):
        """Run a bash script

        Args:
            script: the path of the script to run
            user: the user to run the script as

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
                _uses_shell=True, _raw_params=f"sudo -u {user} bash {script}"
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


