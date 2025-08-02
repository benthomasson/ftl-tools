from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class LineInFile(Tool):
    name = "lineinfile_tool"
    module = "lineinfile"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self, line: str, path: str, state: str = "present", regexp: str = None
    ) -> bool:
        """Add a line to a file

        Args:
            line: the line to add
            state: one of present or absent
            path: the path to the file
            regexp: the regular expression of the line to replace

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "lineinfile",
            self.state["gate_cache"],
            module_args=dict(line=line, state=state, path=path, regexp=regexp),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)


class AddLineToFile(Tool):
    name = "addlinetofile_tool"
    module = "lineinfile"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self,
        line: str,
        path: str,
    ) -> bool:
        """Add a line to a file

        Args:
            line: the line to add
            path: the path to the file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "lineinfile",
            self.state["gate_cache"],
            module_args=dict(line=line, state="present", path=path),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)


class ReplaceLineInFile(Tool):
    name = "replacelineinfile_tool"
    module = "lineinfile"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, line: str, path: str, pattern: str = None) -> bool:
        """Replace a line in a file with another line

        Args:
            line: the line to add
            pattern: the line to replace
            path: the path to the file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "lineinfile",
            self.state["gate_cache"],
            module_args=dict(line=line, state="present", path=path, regexp=pattern),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)