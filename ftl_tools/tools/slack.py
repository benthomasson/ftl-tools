from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class Slack(Tool):
    name = "slack_tool"
    module = "slack"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, msg: str) -> bool:
        """Sends a message to slack.

        Args:
            msg: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["localhost"],
            self.state["modules"],
            "slack",
            self.state["gate_cache"],
            module_args=dict(msg=msg, token=str(self.state["secrets"]["SLACK_TOKEN"])),
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)