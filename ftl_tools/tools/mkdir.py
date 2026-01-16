#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class Mkdir(AutomationTool):
    name = "mkdir"
    description = "Make a directory on the remote machine"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, name: str):
        """Make a directory on the remote machine

        Args:
            name: The name of the directory

        Returns:
            True on successful completion
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        ftl.mkdir_sync(
            self.context.inventory,
            self.context.gate_cache,
            name=name,
            loop=getattr(self.context, "loop", None),
        )

        display_results({}, self.context.console, getattr(self.context, "log", None))

        return True