from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class Discord(Tool):
    name = "discord_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, message: str) -> bool:
        """Sends a message to discord.

        Args:
            message: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["localhost"],
            self.state["modules"],
            "discord",
            self.state["gate_cache"],
            module_args=dict(
                content=message,
                webhook_token=str(self.state["secrets"]["DISCORD_TOKEN"]),
                webhook_id=self.state["discord_channel"],
            ),
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)