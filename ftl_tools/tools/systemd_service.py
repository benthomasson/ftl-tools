#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class SystemDService(Tool):
    name = "systemd_service_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str = "started", enabled: bool = False) -> bool:
        """Control systemd services

        Args:
            name: the name of the service
            state: one of reloaded, restarted, started, or stopped
            enabled: start on boot

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "systemd_service",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state, enabled=enabled),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)