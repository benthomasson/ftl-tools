#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class Unarchive(Tool):
    name = "unarchive_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Unarchives files from the archive file to the destination directory.

        Args:
            src: the name of the archive
            dest: the destination of the unarchived files

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "unarchive",
            self.state["gate_cache"],
            module_args=dict(src=src, dest=dest, remote_src=True),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)