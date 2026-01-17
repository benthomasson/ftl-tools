#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class SwapFile(AutomationTool):
    name = "swapfile"
    module = "command"
    description = "Creates a swapfile"

    def __call__(self, path: str, size: int, permanent: bool = True):
        """Creates a swapfile

        Args:
            path: The path of the swapfile
            size: The size of the swapfile
            permanent: True if permanent

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        def run_command(command):
            # Prepare module args
            module_args = dict(
                _uses_shell=True,
                _raw_params=command,
                creates=path,
            )
            
            # Add check_mode if in dry run
            if getattr(self.context, 'dry_run', False):
                module_args['_ansible_check_mode'] = True
            
            output = ftl.run_module_sync(
                self.context.inventory,
                self.context.modules,
                "command",
                getattr(self.context, 'gate_cache', None),
                module_args=module_args,
                dependencies=dependencies,
                loop=getattr(self.context, 'loop', None),
                use_gate=getattr(self.context, 'use_gate', False),
            )

            display_results(output, self.context.console, getattr(self.context, 'log', None))

            return output

        output = run_command(
            f"dd if=/dev/zero of={path} bs={size} count={int(size * 1024)} &&"
            f"chmod 600 {path} &&"
            f"mkswap {path} &&"
            f"swapon {path}"
        )

        return output
