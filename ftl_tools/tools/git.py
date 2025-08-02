from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class Git(Tool):
    name = "git_tool"
    module = "git"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, repo: str, dest: str, update: bool = True) -> bool:
        '''Deploy software (or files) from git checkouts

        Args:
            repo: git, SSH, or HTTP(S) protocol address of the git repository
            dest: The path of where the repository should be checked out
            update: If false, do not retrieve new revisions from the origin repository

        Returns:
            boolean
        '''
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            self.module,
            self.state["gate_cache"],
            module_args=dict(repo=repo, dest=dest, update=update),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)