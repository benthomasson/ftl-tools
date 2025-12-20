#!/usr/bin/env python3
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class PodmanVersion(AutomationTool):
    name = "podman_version_tool"
    module = "command"
    description = "Gets the podman version"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self):
        """Gets the podman version

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            self.context.gate_cache,
            module_args=dict(
                _uses_shell=True,
                _raw_params="podman --version",
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


class PodmanPull(AutomationTool):
    name = "podman_pull_tool"
    module = "command"
    description = "Pulls a container image using podman"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, image: str):
        """Pulls a container image using podman

        Args:
            image: the container image to pull

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            self.context.gate_cache,
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"podman pull {image}",
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output


class PodmanRun(AutomationTool):
    name = "podman_run_tool"
    module = "command"
    description = "Runs a container image using podman"

    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, image: str):
        """Runs a container image using podman

        Args:
            image: the container image to run

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, "log", None))

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "command",
            self.context.gate_cache,
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"podman run -it {image}",
            ),
            dependencies=dependencies,
            loop=getattr(self.context, "loop", None),
            use_gate=self.context.use_gate,
        )

        display_results(output, self.context.console, getattr(self.context, "log", None))

        return output
