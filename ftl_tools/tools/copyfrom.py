#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool, safe_join_path


class CopyFrom(AutomationTool):
    name = "copy_from_tool"
    description = "Copy file from remote machine locally"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, src: str, dest: str):
        """Copy file from remote machine locally

        Args:
            src: The remote source of the file
            dest: The local destination of the file

        Returns:
            True if successful, False if destination path is invalid
        """

        dest = safe_join_path(getattr(self.context, "workspace", "."), dest)

        if dest is None:
            return False

        display_tool(self, self.context.console, getattr(self.context, "log", None))
        ftl.copy_from_sync(
            self.context.inventory,
            self.context.gate_cache,
            src=src,
            dest=dest,
            loop=getattr(self.context, "loop", None),
        )

        display_results({}, self.context.console, getattr(self.context, "log", None))

        return True