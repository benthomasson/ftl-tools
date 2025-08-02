#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class User(Tool):
    name = "user_tool"
    module = "user"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, group: str) -> bool:
        """Create a user

        Args:
            name: the name of the user
            group: the group the user should belong to

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "user",
            self.state["gate_cache"],
            module_args=dict(
                name=name,
                create_home=True,
                group=group,
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)