#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Timezone(AutomationTool):
    name = "timezone"
    module = "timezone"
    description = "Configure timezone setting"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, name: str):
        """Configure timezone setting

        Args:
            name: Name of the timezone for the system clock

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            self.module,
            self.context.gate_cache,
            module_args=dict(name=name),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output