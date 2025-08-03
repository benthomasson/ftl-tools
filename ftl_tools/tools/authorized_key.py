import os
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema
import faster_than_light as ftl
from ftl_tools.utils import dependencies, display_results, display_tool


class AuthorizedKey(Tool):
    name = "authorized_key_tool"
    module = "authorized_key"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, user: str, key_file: str, state: str = "present") -> bool:
        """Manage authorized keys and upload public keys to the remote node

        Args:
            user: the name of the user
            state: one of present or absent
            key_file: the path to the file containing the public key_file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        key_file = os.path.abspath(os.path.expanduser(key_file))
        if not os.path.exists(key_file) or not os.path.isfile(key_file):
            raise Exception(f"{key_file} does not exist")
        with open(key_file) as f:
            key_value = f.read()
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "authorized_key",
            self.state["gate_cache"],
            module_args=dict(user=user, state=state, key=key_value),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return output

    description, inputs, output_type = get_json_schema(forward)
