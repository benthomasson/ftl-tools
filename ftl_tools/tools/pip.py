from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class Pip(Tool):
    name = "pip_tool"
    module = "pip"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str = "present") -> bool:
        """Install python packages using pip

        Args:
            name: the name of the package
            state: one of latest, present, absent

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "pip",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)


class PipRequirements(Tool):
    name = "pip_requirements_tool"
    module = "pip"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, requirements: str, venv: str) -> bool:
        """Install dependencies from python requirements.txt files using pip.

        Args:
            requirements: the path to the requirements.txt file
            venv: the path to the virtual environment to install the packages to

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "pip",
            self.state["gate_cache"],
            module_args=dict(
                requirements=requirements,
                virtualenv=venv,
                virtualenv_command="python3 -m venv",
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)