#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_tools.base_tool import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Bash(AutomationTool):
    name = "bash_tool"
    module = "command"
    description = "Run a bash script"

    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, script: str, user: str):
        """Run a bash script

        Args:
            script: the path of the script to run
            user: the user to run the script as

        Returns:
            Module execution result
        """
        display_tool(self, self.state["console"], self.state.get("log"))

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state.get("gate_cache"),
            module_args=dict(
                _uses_shell=True, _raw_params=f"sudo -u {user} bash {script}"
            ),
            dependencies=dependencies,
            loop=self.state.get("loop"),
            use_gate=self.state.get("gate"),
        )

        display_results(output, self.state["console"], self.state.get("log"))

        return output


# Create function interface for ftl-automation
def bash_tool(inventory, modules, console, script: str, user: str, **kwargs):
    """Run a bash script.
    
    Args:
        inventory: Target systems/hosts configuration
        modules: Available automation modules
        console: Rich console for formatted output
        script: the path of the script to run
        user: the user to run the script as
        **kwargs: Additional context
        
    Returns:
        Module execution result
    """
    tool = Bash(inventory, modules, console, **kwargs)
    return tool(script=script, user=user)