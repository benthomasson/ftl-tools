#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import display_results, display_tool, safe_join_path


class CopyFrom(Tool):
    name = "copy_from_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Copy file from remote machine locally

        Args:
            src: The remote source of the file
            dest: The local destination of the file

        Returns:
            boolean
        """

        dest = safe_join_path(self.state["workspace"], dest)

        if dest is None:
            return False

        display_tool(self, self.state["console"], self.state["log"])
        ftl.copy_from_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            src=src,
            dest=dest,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)