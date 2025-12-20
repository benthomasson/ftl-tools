#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool, safe_join_path


class Template(AutomationTool):
    name = "template_tool"
    description = "Template a local file and copy the result to a remote machine"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, src: str, dest: str):
        """Template a local file and copy the result to a remote machine.

        Args:
            src: The source of the template to be copied
            dest: The destination of the file

        Returns:
            Module execution result or False if source path is invalid
        """

        src = safe_join_path(getattr(self.context, "workspace", "."), src)

        if src is None:
            return False

        display_tool(self, self.context.console, getattr(self.context, "log", None))
        output = ftl.template_sync(
            self.context.inventory,
            self.context.gate_cache,
            src=src,
            dest=dest,
            loop=getattr(self.context, "loop", None),
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output
