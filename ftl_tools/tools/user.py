#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class User(AutomationTool):
    name = "user"
    module = "user"
    description = "Create a user"

    def __call__(self, name: str, group: str):
        """Create a user

        Args:
            name: the name of the user
            group: the group the user should belong to

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        # Prepare module args for user operation
        user_module_args = dict(
            name=name,
            create_home=True,
            group=group,
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            user_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "user",
            getattr(self.context, 'gate_cache', None),
            module_args=user_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output