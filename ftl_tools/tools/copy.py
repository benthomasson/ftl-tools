#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import display_results, display_tool, safe_join_path


class Copy(Tool):
    name = "copy_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Copy file to remote machine

        Args:
            src: The source of the file
            dest: The destination of the file

        Returns:
            boolean
        """

        src = safe_join_path(self.state["workspace"], src)

        if src is None:
            return False

        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.copy_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            src=safe_join_path(self.state["workspace"], src),
            dest=dest,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)