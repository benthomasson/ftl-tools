#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import display_results, display_tool


class Mkdir(Tool):
    name = "mkdir_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str) -> bool:
        """Make a directory on the remote machine

        Args:
            name: The name of the directory

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        ftl.mkdir_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            name=name,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)