#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Dnf(AutomationTool):
    name = "dnf"
    module = "dnf"
    description = "Control dnf packages"

    def __call__(self, name: str, state: str):
        """Control dnf packages

        Args:
            name: the name of the package, use '*' for all packages
            state: one of latest, present, absent

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        # Prepare module args for dependency installation
        dep_module_args = dict(
            _uses_shell=True,
            _raw_params=f"dnf install -y python3-dnf",
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            dep_module_args['_ansible_check_mode'] = True

        # Ensure that python3-dnf is installed so the dnf module doesn't fail
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            getattr(self.context, 'gate_cache', None),
            module_args=dep_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        # Prepare module args for dnf operation
        dnf_module_args = dict(name=name, state=state)
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            dnf_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "dnf",
            getattr(self.context, 'gate_cache', None),
            module_args=dnf_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output
