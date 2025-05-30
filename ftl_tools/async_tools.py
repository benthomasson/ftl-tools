#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import os
import faster_than_light as ftl
import shutil
import logging
import yaml
import json
from linode_api4 import LinodeClient

from rich.console import Console
from rich.pretty import pprint

from ftl_automation_agent import console
from rich.rule import Rule


logger = logging.getLogger("tools")

dependencies = [
    "ftl_module_utils @ git+https://github.com/benthomasson/ftl_module_utils@main",
    "ftl_collections @ git+https://github.com/benthomasson/ftl-collections@main",
]


def write_or_print(output, console, log):

    if log is None:
        console.print(output)
    else:
        log.write(output)


def display_tool(tool, console, log):
    write_or_print(Rule(title=f"\n[green]TOOL [white]\[{tool.name}]", align="left"), console, log)


def display_results(output, console, log):
    if log is None:
        #pprint(output, console=console)
        for name, results in output.items():
            if results.get("failed"):
                raise Exception(results.get("msg"))
            if results.get("changed"):
                console.print(f"[yellow] changed: [{name}]")
            else:
                console.print(f"[green] ok: [{name}]")
        console.print("")
        console.print_json(json.dumps(output))
    else:
        #log.write(output)
        for name, results in output.items():
            if results.get("failed"):
                raise Exception(results.get("msg"))
            if results.get("changed"):
                log.write(f"[yellow] changed: [{name}]")
            else:
                log.write(f"[green] ok: [{name}]")
        log.write("")
        log.write(output)


class Service(Tool):
    name = "service"
    module = "service"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str, state: str) -> bool:
        """Manager a service

        Args:
            name: the name of the service
            state: one of started, restarted, or stopped

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])

        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "service",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class LineInFile(Tool):
    name = "lineinfile"
    module = "lineinfile"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(
        self, line: str, path: str, state: str = "present", regexp: str = None
    ) -> bool:
        """Add a line to a file

        Args:
            line: the line to add
            state: one of present or absent
            path: the path to the file
            regexp: the regular expression of the line to replace

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "lineinfile",
            self.state["gate_cache"],
            module_args=dict(line=line, state=state, path=path, regexp=regexp),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class AuthorizedKey(Tool):
    name = "authorized_key"
    module = "authorized_key"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, user: str, key: str, state: str = "present") -> bool:
        """Manage authorized keys and upload public keys to the remote node

        Args:
            user: the name of the user
            state: one of present or absent
            key: the path to the file containing the public key

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        key = os.path.abspath(os.path.expanduser(key))
        if not os.path.exists(key) or not os.path.isfile(key):
            raise Exception(f"{key} does not exist")
        with open(key) as f:
            key_value = f.read()
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "authorized_key",
            self.state["gate_cache"],
            module_args=dict(user=user, state=state, key=key_value),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class User(Tool):
    name = "user"
    module = "user"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str, group: str) -> bool:
        """Create a user

        Args:
            name: the name of the user
            group: the group the user should belong to

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "user",
            self.state["gate_cache"],
            module_args=dict(
                name=name,
                create_home=True,
                group=group,
            ),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Dnf(Tool):
    name = "dnf"
    module = "dnf"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str, state: str) -> bool:
        """Control dnf packages

        Args:
            name: the name of the package, use '*' for all packages
            state: one of latest, present, absent

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "dnf",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Apt(Tool):
    name = "apt"
    module = "apt"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, update_cache: bool = False, upgrade: str = "no") -> bool:
        """Control apt packages

        Args:
            update_cache: Update the cache if true
            upgrade: Either yes, safe, or no.

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "apt",
            self.state["gate_cache"],
            module_args=dict(update_cache=update_cache, upgrade=upgrade),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Hostname(Tool):
    name = "hostname"
    module = "hostname"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str) -> bool:
        """Sets the hostname of the machine.

        Args:
            name: the name to set

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "hostname",
            self.state["gate_cache"],
            module_args=dict(name=name),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Slack(Tool):
    name = "slack"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, msg: str) -> bool:
        """Sends a message to slack.

        Args:
            msg: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["localhost"],
            self.state["modules"],
            "slack",
            self.state["gate_cache"],
            module_args=dict(msg=msg, token=self.state["slack_token"]),
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Discord(Tool):
    name = "discord"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, message: str) -> bool:
        """Sends a message to discord.

        Args:
            message: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["localhost"],
            self.state["modules"],
            "discord",
            self.state["gate_cache"],
            module_args=dict(
                content=message,
                webhook_token=self.state["discord_token"],
                webhook_id=self.state["discord_channel"],
            ),
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class FirewallD(Tool):
    name = "firewalld"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, port: str, state: str, permanent: bool) -> bool:
        """Configure firewalld

        Args:
            port: The port/protocol like 8081/tcp
            state: One of enabled or disabled
            permanent: True if permanent

        Returns:
            boolean
        """
        if isinstance(port, int):
            port = f"{port}/tcp"
        elif port.endswith("/tcp"):
            pass
        elif port.endswith("/udp"):
            pass
        else:
            port = f"{port}/tcp"
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "firewalld",
            self.state["gate_cache"],
            module_args=dict(
                port=port,
                state=state,
                permanent=permanent,
            ),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Linode(Tool):
    name = "linode"
    module = None

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str) -> bool:
        """Provisions a new linode server

        Args:
            name: the name of the server

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])

        pprint(self.state["inventory"], console=console)

        # Create a Linode API client
        with open(os.path.expanduser("~/secrets/linode_token")) as f:
            client = LinodeClient(f.read().strip())

        with open(os.path.expanduser("~/secrets/linode1")) as f:
            root_pass = f.read().strip()

        my_linodes = client.linode.instances()

        for instance in my_linodes:
            if instance.label == name:
                console.print(f"Already created {name}")
                return True

        # Create a new Linode
        new_linode = client.linode.instance_create(
            ltype="g6-nanode-1",
            region="us-southeast",
            image="private/31658563",
            label=name,
            root_pass=root_pass,
            authorized_users=["benthomasson"],
        )

        # Print info about the Linode
        console.print("Linode IP:", new_linode.ipv4[0])

        host_data = {
            "ansible_user": "root",
            "ansible_host": new_linode.ipv4[0],
            "ansible_python_interpreter": "/usr/bin/python3",
            "host_name": name,
        }
        if self.state["inventory"].get("all") is None:
            self.state["inventory"]["all"] = {}
        if self.state["inventory"]["all"].get("hosts") is None:
            self.state["inventory"]["all"]["hosts"] = {}
        self.state["inventory"]["all"]["hosts"][name] = host_data

        with open("inventory.yml", "w") as f:
            f.write(yaml.safe_dump(self.state["inventory"]))

        pprint(self.state["inventory"], console=console)

        return True

    description, inputs, output_type = get_json_schema(forward)


class SwapFile(Tool):
    name = "swapfile"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, location: str, size: int, permanent: bool = True) -> bool:
        """Creates a swapfile

        Args:
            location: The location of the swapfile
            size: The size of the swapfile
            permanent: True if permanent

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])

        async def run_command(command):

            output = await ftl.run_module(
                self.state["inventory"],
                self.state["modules"],
                "command",
                self.state["gate_cache"],
                module_args=dict(
                    _uses_shell=True,
                    _raw_params=command,
                    creates=location,
                ),
                dependencies=dependencies,
                use_gate=self.state["gate"],
            )

            display_results(output, self.state['console'], self.state['log'])

        await run_command(f"dd if=/dev/zero of={location} bs={size} count={int(size * 1024)} &&"
                    f"chmod 600 {location} &&"
                    f"mkswap {location} &&"
                    f"swapon {location}")

        return True

    description, inputs, output_type = get_json_schema(forward)


class Chown(Tool):
    name = "chown"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, user: str, location: str) -> bool:
        """Changes the ownership of a directory and the files in it.

        Args:
            location: The location of the swapfile
            user: The size of the swapfile

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])

        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"chown -R {user} {location}",
            ),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Mkdir(Tool):
    name = "mkdir"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str) -> bool:
        """Make a directory on the remote machine

        Args:
            name: The name of the directory

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        ftl.mkdir(
            self.state["inventory"],
            self.state["gate_cache"],
            name=name,
        )

        display_results({}, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Copy(Tool):
    name = "copy"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, src: str, dest: str) -> bool:
        """Copy file to remote machine

        Args:
            src: The source of the file
            dest: The destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        ftl.copy(
            self.state["inventory"],
            self.state["gate_cache"],
            src=src,
            dest=dest,
        )

        display_results({}, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class CopyFrom(Tool):
    name = "copy_from"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, src: str, dest: str) -> bool:
        """Copy file from remote machine locally

        Args:
            src: The remote source of the file
            dest: The local destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        ftl.copy_from(
            self.state["inventory"],
            self.state["gate_cache"],
            src=src,
            dest=dest,
        )

        display_results({}, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class SystemDService(Tool):
    name = "systemd_service"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str, state: str = "started", enabled: bool = False) -> bool:
        """Control systemd services

        Args:
            name: the name of the service
            state: one of reloaded, restarted, started, or stopped
            enabled: start on boot

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "systemd_service",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state, enabled=enabled),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class GetURL(Tool):
    name = "get_url"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, url: str, dest: str) -> bool:
        """Downloads a file

        Args:
            url: The url of the file
            dest: the destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "get_url",
            self.state["gate_cache"],
            module_args=dict(
                url=url,
                dest=dest,
            ),
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Pip(Tool):
    name = "pip"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    async def forward(self, name: str, state: str = "present") -> bool:
        """Control dnf packages

        Args:
            name: the name of the package
            state: one of latest, present, absent

        Returns:
            boolean
        """
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(
            self.state["inventory"],
            self.state["modules"],
            "pip",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            use_gate=self.state["gate"],
        )

        display_results(output, self.state['console'], self.state['log'])

        return True

    description, inputs, output_type = get_json_schema(forward)


__all__ = [
    "Service",
    "LineInFile",
    "AuthorizedKey",
    "User",
    "Dnf",
    "Apt",
    "Hostname",
    "Slack",
    "Discord",
    "Linode",
    "FirewallD",
    "SwapFile",
    "Chown",
    "Copy",
    "CopyFrom",
    "SystemDService",
    "GetURL",
    "Pip",
]


if __name__ == "__main__":
    import sys
    import inspect

    print("Tools")
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if obj == Tool:
                continue
            tool = obj
            description, inputs, output_type = get_json_schema(tool.forward)
            print(f"* {tool.name} - {description}")
