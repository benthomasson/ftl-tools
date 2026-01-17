#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Certbot(AutomationTool):
    name = "certbot"
    module = "command"
    description = "Configure SSL certificates using certbot for nginx"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, server_name: str, email: str):
        """Configures SSL certificates using certbot for nginx

        Args:
            server_name: The name of server to configure SSL certificates for.
            email: The email address to register with

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        # Prepare module args
        module_args = dict(
            _uses_shell=True,
            _raw_params=f"certbot --nginx -n -d {server_name} --agree-tos --email {email}",
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
