#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class LineInFile(AutomationTool):
    name = "lineinfile"
    module = "lineinfile"
    description = "Add or modify a line in a file"

    def __call__(self, line: str, path: str, state: str = "present", regexp: str = None):
        """Add a line to a file

        Args:
            line: the line to add
            state: one of present or absent
            path: the path to the file
            regexp: the regular expression of the line to replace

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "lineinfile",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(line=line, state=state, path=path, regexp=regexp),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output


class AddLineToFile(AutomationTool):
    name = "addlinetofile"
    module = "lineinfile"
    description = "Add a line to a file"

    def __call__(self, line: str, path: str):
        """Add a line to a file

        Args:
            line: the line to add
            path: the path to the file

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "lineinfile",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(line=line, state="present", path=path),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output


class ReplaceLineInFile(AutomationTool):
    name = "replacelineinfile"
    module = "lineinfile"
    description = "Replace a line in a file with another line"

    def __call__(self, line: str, path: str, pattern: str = None):
        """Replace a line in a file with another line

        Args:
            line: the line to add
            pattern: the line to replace
            path: the path to the file

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "lineinfile",
            getattr(self.context, 'gate_cache', None),
            module_args=dict(line=line, state="present", path=path, regexp=pattern),
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output