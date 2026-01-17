#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class FirewallD(AutomationTool):
    name = "firewalld"
    module = "firewalld"
    description = "Configure firewalld"

    def __call__(self, port: str, state: str, protocol: str = None, permanent: bool = True):
        """Configure firewalld

        Args:
            port: The port to control
            state: One of enabled or disabled
            protocol: tcp or udp
            permanent: True if permanent

        Returns:
            Module execution result
        """
        if isinstance(port, int):
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        elif port.endswith("/tcp"):
            pass
        elif port.endswith("/udp"):
            pass
        else:
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        # Prepare module args for firewalld operation
        firewalld_module_args = dict(
            port=port,
            state=state,
            permanent=permanent,
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            firewalld_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "firewalld",
            getattr(self.context, 'gate_cache', None),
            module_args=firewalld_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output