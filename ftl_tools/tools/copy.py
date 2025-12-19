#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool, safe_join_path


class Copy(AutomationTool):
    name = "copy"
    module = None  # Uses ftl.copy_sync directly, not a module
    description = "Copy file to remote machine"

    def __call__(self, src: str, dest: str):
        """Copy file to remote machine

        Args:
            src: The source of the file
            dest: The destination of the file

        Returns:
            Copy operation result
        """
        workspace = getattr(self.context, 'workspace', '.')
        src = safe_join_path(workspace, src)

        if src is None:
            return False

        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.copy_sync(
            self.context.inventory,
            getattr(self.context, 'gate_cache', None),
            src=safe_join_path(workspace, src),
            dest=dest,
            loop=getattr(self.context, 'loop', None),
        )

        display_results({}, self.context.console, getattr(self.context, 'log', None))

        return output