#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class SwapFile(Tool):
    name = "swapfile_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, location: str, size: int, permanent: bool = True) -> bool:
        """Creates a swapfile

        Args:
            location: The location of the swapfile
            size: The size of the swapfile
            permanent: True if permanent

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        def run_command(command):

            output = ftl.run_module_sync(
                self.state["inventory"],
                self.state["modules"],
                "command",
                self.state["gate_cache"],
                module_args=dict(
                    _uses_shell=True,
                    _raw_params=command,
                    creates=location,
                ),
                dependencies=dependencies,
                loop=self.state["loop"],
                use_gate=self.state["gate"],
            )

            display_results(output, self.state["console"], self.state["log"])

            return output

        output = run_command(
            f"dd if=/dev/zero of={location} bs={size} count={int(size * 1024)} &&"
            f"chmod 600 {location} &&"
            f"mkswap {location} &&"
            f"swapon {location}"
        )

        return output

    description, inputs, output_type = get_json_schema(forward)