#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class GetURL(AutomationTool):
    name = "get_url"
    module = "get_url"
    description = "Downloads a file from a URL"

    def __call__(self, url: str, dest: str):
        """Downloads a file

        Args:
            url: The url of the file
            dest: the destination of the file

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "get_url",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(
                url=url,
                dest=dest,
            ),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output