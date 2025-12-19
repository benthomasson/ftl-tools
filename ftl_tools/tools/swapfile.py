#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class SwapFile(AutomationTool):
    name = "swapfile"
    module = "command"
    description = "Creates a swapfile"

    def __call__(self, location: str, size: int, permanent: bool = True):
        """Creates a swapfile

        Args:
            location: The location of the swapfile
            size: The size of the swapfile
            permanent: True if permanent

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        def run_command(command):
            output = ftl.run_module_sync(
                self.context.inventory,
                self.context.modules,
                "command",
                getattr(self.context, 'gate_cache', None),
                module_args=dict(
                    _uses_shell=True,
                    _raw_params=command,
                    creates=location,
                ),
                dependencies=dependencies,
                loop=getattr(self.context, 'loop', None),
                use_gate=getattr(self.context, 'use_gate', False),
            )

            display_results(output, self.context.console, getattr(self.context, 'log', None))

            return output

        output = run_command(
            f"dd if=/dev/zero of={location} bs={size} count={int(size * 1024)} &&"
            f"chmod 600 {location} &&"
            f"mkswap {location} &&"
            f"swapon {location}"
        )

        return output