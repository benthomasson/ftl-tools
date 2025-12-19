#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Apt(AutomationTool):
    name = "apt"
    module = "apt"
    description = "Control apt packages"

    def __call__(self, update_cache: bool = False, upgrade: str = "no"):
        """Control apt packages

        Args:
            update_cache: Update the cache if true
            upgrade: Either yes, safe, or no.

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "apt",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(update_cache=update_cache, upgrade=upgrade),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output