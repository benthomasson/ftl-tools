#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class Chown(Tool):
    name = "chown_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, user: str, location: str) -> bool:
        """Changes the ownership of a directory and the files in it.

        Args:
            location: The location of the swapfile
            user: The new owner of the location

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"chown -R {user} {location}",
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)