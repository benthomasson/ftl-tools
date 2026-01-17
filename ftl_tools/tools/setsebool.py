#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class SetSeBool(AutomationTool):
    name = "setsebool"
    module = "command"
    description = "Sets SELinux boolean values"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, name: str, value: str):
        """Sets SELinux boolean values

        Args:
            name: The name of the boolean to set
            value: The value to set. One of `on` or `off`.

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        # Prepare module args
        module_args = dict(
            _uses_shell=True,
            _raw_params=f"setsebool {name} {value}",
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            self.context.gate_cache,
            module_args=module_args,
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output
