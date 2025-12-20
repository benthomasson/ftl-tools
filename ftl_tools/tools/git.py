#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class Git(AutomationTool):
    name = "git_tool"
    module = "git"
    description = "Deploy software (or files) from git checkouts"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, repo: str, dest: str, update: bool = True):
        """Deploy software (or files) from git checkouts

        Args:
            repo: git, SSH, or HTTP(S) protocol address of the git repository
            dest: The path of where the repository should be checked out
            update: If false, do not retrieve new revisions from the origin repository

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            self.module,
            self.context.gate_cache,
            module_args=dict(repo=repo, dest=dest, update=update),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output