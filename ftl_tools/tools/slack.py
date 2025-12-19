#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Slack(AutomationTool):
    name = "slack"
    module = "slack"
    description = "Sends a message to slack"

    def __call__(self, msg: str, channel: str = None):
        """Sends a message to slack.

        Args:
            msg: the message to send
            channel: the channel to send to (optional)

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        # Build module args with required token
        module_args = {
            "msg": msg,
            "token": str(self.context.secrets["SLACK_TOKEN"])
        }
        
        # Add optional channel if provided
        if channel:
            module_args["channel"] = channel
            
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "slack",
            getattr(self.context, 'gate_cache', None),
            module_args=module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output