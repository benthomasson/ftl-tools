from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool, safe_join_path




class Template(Tool):
    name = "template_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str, **kwargs: dict) -> bool:
        """Template a local file and copy the result to a remote machine

        Args:
            src: The source of the template to be copied
            dest: The destination of the file
            kwargs: Values to be inserted into the template

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
            src=src,
            dest=dest,
            loop=self.state["loop"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)
