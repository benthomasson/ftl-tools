#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Service(AutomationTool):
    name = "service"
    module = "service"
    description = "Manage a service"

    def __call__(self, name: str, state: str):
        """Manage a service

        Args:
            name: the name of the service
            state: one of started, restarted, or stopped

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        # Prepare module args for service operation
        service_module_args = dict(name=name, state=state)
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            service_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "service",
            getattr(self.context, 'gate_cache', None),
            module_args=service_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output