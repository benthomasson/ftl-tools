#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class SystemDService(AutomationTool):
    name = "systemd_service"
    module = "systemd_service"
    description = "Control systemd services"

    def __call__(self, name: str, state: str = "started", enabled: bool = False):
        """Control systemd services

        Args:
            name: the name of the service
            state: one of reloaded, restarted, started, or stopped
            enabled: start on boot

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "systemd_service",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(name=name, state=state, enabled=enabled),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output