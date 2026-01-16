#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Chmod(AutomationTool):
    name = "chmod"
    module = "command"
    description = "Changes the permissions of a file or directory"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, permissions: str, location: str):
        """Changes the permissions of a file or directory.

        Args:
            permissions: The permissions to set (e.g., "755", "644")
            location: The location of the file or directory

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
                _raw_params=f"chmod {permissions} {location}",
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output