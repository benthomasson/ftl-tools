#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Hostname(AutomationTool):
    name = "hostname"
    module = "hostname"
    description = "Sets the hostname of the machine"

    def __call__(self, name: str):
        """Sets the hostname of the machine.

        Args:
            name: the name to set

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "hostname",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(name=name),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output
