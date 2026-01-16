#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Unarchive(AutomationTool):
    name = "unarchive"
    module = "unarchive"
    description = "Unarchives files from the archive file to the destination directory"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, src: str, dest: str):
        """Unarchives files from the archive file to the destination directory.

        Args:
            src: the name of the archive
            dest: the destination of the unarchived files

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "unarchive",
            self.context.gate_cache,
            module_args=dict(src=src, dest=dest, remote_src=True),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output