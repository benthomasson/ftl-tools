#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Pip(AutomationTool):
    name = "pip"
    module = "pip"
    description = "Install python packages using pip"

    def __call__(self, name: str, state: str = "present"):
        """Install python packages using pip

        Args:
            name: the name of the package
            state: one of latest, present, absent

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        # Prepare module args
        module_args = dict(name=name, state=state)
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            module_args['_ansible_check_mode'] = True
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "pip",
            getattr(self.context, 'gate_cache', None),
            module_args=module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output


class PipRequirements(AutomationTool):
    name = "pip_requirements"
    module = "pip"
    description = "Install dependencies from python requirements.txt files using pip"

    def __call__(self, requirements: str, venv: str):
        """Install dependencies from python requirements.txt files using pip.

        Args:
            requirements: the path to the requirements.txt file
            venv: the path to the virtual environment to install the packages to

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        # Prepare module args
        module_args = dict(
            requirements=requirements,
            virtualenv=venv,
            virtualenv_command="python3 -m venv",
        )
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            module_args['_ansible_check_mode'] = True
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "pip",
            getattr(self.context, 'gate_cache', None),
            module_args=module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output