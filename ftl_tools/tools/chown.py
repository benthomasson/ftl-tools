#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Chown(AutomationTool):
    name = "chown"
    module = "command"
    description = "Changes the ownership of a directory and the files in it"

    def __call__(self, user: str, path: str):
        """Changes the ownership of a directory and the files in it.

        Args:
            user: The new owner of the path
            path: The path to change ownership

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        # Prepare module args for chown operation
        chown_module_args = dict(
            _uses_shell=True,
            _raw_params=f"chown -R {user} {path}",
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            chown_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            getattr(self.context, 'gate_cache', None),
            module_args=chown_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output
