#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import faster_than_light as ftl

from ftl_tools.utils import dependencies, display_results, display_tool


class FirewallD(Tool):
    name = "firewalld_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self, port: str, state: str, protocol: str = None, permanent: bool = True
    ) -> bool:
        """Configure firewalld

        Args:
            port: The port to control
            state: One of enabled or disabled
            protocol: tcp or udp
            permanent: True if permanent

        Returns:
            boolean
        """
        if isinstance(port, int):
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        elif port.endswith("/tcp"):
            pass
        elif port.endswith("/udp"):
            pass
        else:
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "firewalld",
            self.state["gate_cache"],
            module_args=dict(
                port=port,
                state=state,
                permanent=permanent,
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)