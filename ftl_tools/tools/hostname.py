#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_tools.base_tool import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Hostname(AutomationTool):
    name = "hostname_tool"
    module = "hostname"
    description = "Sets the hostname of the machine"

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

    def forward(self, name: str):
        """Sets the hostname of the machine.

        Args:
            name: the name to set

        Returns:
            Module execution result
        """
        display_tool(self, self.state["console"], self.state.get('log'))
        
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "hostname",
            self.state.get("gate_cache"),
            module_args=dict(name=name),
            dependencies=dependencies,
            loop=self.state.get("loop"),
            use_gate=self.state.get("gate"),
        )

        display_results(output, self.state["console"], self.state.get('log'))

        return output


# Create function interface for ftl-automation
def hostname_tool(inventory, modules, console, name: str, **kwargs):
    """Sets the hostname of the machine.
    
    Args:
        inventory: Target systems/hosts configuration
        modules: Available automation modules
        console: Rich console for formatted output  
        name: the name to set
        **kwargs: Additional context
        
    Returns:
        Module execution result
    """
    tool = Hostname(inventory, modules, console, **kwargs)
    return tool(name=name)