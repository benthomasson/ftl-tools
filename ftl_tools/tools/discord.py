#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Discord(AutomationTool):
    name = "discord"
    module = "discord"
    description = "Sends a message to discord"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, message: str):
        """Sends a message to discord.

        Args:
            message: the message to send

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))
        
        # Prepare module args
        module_args = dict(
            content=message,
            webhook_token=str(self.context.secrets["DISCORD_TOKEN"]),
            webhook_id=getattr(self.context, "discord_channel", None),
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            module_args['_ansible_check_mode'] = True
        
        output = ftl.run_module_sync(
            self.context.localhost,
            self.context.modules,
            "discord",
            self.context.gate_cache,
            module_args=module_args,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output