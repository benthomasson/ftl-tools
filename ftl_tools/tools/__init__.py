#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import os
import faster_than_light as ftl
import logging
import yaml
from linode_api4 import LinodeClient

from rich.pretty import pprint

from ftl_automation_agent import console

from ftl_tools.utils import dependencies, display_results, display_tool

from .timezone import Timezone
from .git import Git
from .podman import PodmanVersion, PodmanRun, PodmanPull


logger = logging.getLogger("tools")


class Service(Tool):
    name = "service_tool"
    module = "service"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str) -> bool:
        """Manager a service

        Args:
            name: the name of the service
            state: one of started, restarted, or stopped

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "service",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class LineInFile(Tool):
    name = "lineinfile_tool"
    module = "lineinfile"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
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
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "lineinfile",
            self.state["gate_cache"],
            module_args=dict(line=line, state=state, path=path, regexp=regexp),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class AuthorizedKey(Tool):
    name = "authorized_key_tool"
    module = "authorized_key"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, user: str, key: str, state: str = "present") -> bool:
        """Manage authorized keys and upload public keys to the remote node

        Args:
            user: the name of the user
            state: one of present or absent
            key: the path to the file containing the public key

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        key = os.path.abspath(os.path.expanduser(key))
        if not os.path.exists(key) or not os.path.isfile(key):
            raise Exception(f"{key} does not exist")
        with open(key) as f:
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

        return True

    description, inputs, output_type = get_json_schema(forward)


class User(Tool):
    name = "user_tool"
    module = "user"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, group: str) -> bool:
        """Create a user

        Args:
            name: the name of the user
            group: the group the user should belong to

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
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
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Dnf(Tool):
    name = "dnf_tool"
    module = "dnf"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str) -> bool:
        """Control dnf packages

        Args:
            name: the name of the package, use '*' for all packages
            state: one of latest, present, absent

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "dnf",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Apt(Tool):
    name = "apt_tool"
    module = "apt"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, update_cache: bool = False, upgrade: str = "no") -> bool:
        """Control apt packages

        Args:
            update_cache: Update the cache if true
            upgrade: Either yes, safe, or no.

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "apt",
            self.state["gate_cache"],
            module_args=dict(update_cache=update_cache, upgrade=upgrade),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Hostname(Tool):
    name = "hostname_tool"
    module = "hostname"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str) -> bool:
        """Sets the hostname of the machine.

        Args:
            name: the name to set

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "hostname",
            self.state["gate_cache"],
            module_args=dict(name=name),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Slack(Tool):
    name = "slack_tool"
    module = "slack"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, msg: str) -> bool:
        """Sends a message to slack.

        Args:
            msg: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["localhost"],
            self.state["modules"],
            "slack",
            self.state["gate_cache"],
            module_args=dict(msg=msg, token=self.state["slack_token"]),
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Discord(Tool):
    name = "discord_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, message: str) -> bool:
        """Sends a message to discord.

        Args:
            message: the message to send

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["localhost"],
            self.state["modules"],
            "discord",
            self.state["gate_cache"],
            module_args=dict(
                content=message,
                webhook_token=self.state["discord_token"],
                webhook_id=self.state["discord_channel"],
            ),
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class FirewallD(Tool):
    name = "firewalld_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self, port: str, state: str, protocol: str = None, permanent: bool = True
    ) -> bool:
        """Configure firewalld

        Args:
            port: The port to control
            state: One of enabled or disabled
            protocol: tcp or udp
            permanent: True if permanent

        Returns:
            boolean
        """
        if isinstance(port, int):
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        elif port.endswith("/tcp"):
            pass
        elif port.endswith("/udp"):
            pass
        else:
            if protocol:
                port = f"{port}/{protocol}"
            else:
                port = f"{port}/tcp"
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
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
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Linode(Tool):
    name = "linode_tool"
    module = None

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self, name: str, image: str = "linode/fedora40", ltype: str = "g6-nanode-1"
    ) -> bool:
        """Provisions a new linode server

        Args:
            name: the name of the server
            image: the name of the server image to use
            ltype: the linode type of the server

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

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
            ltype=ltype,
            region="us-southeast",
            image=image,
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
    name = "swapfile_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, location: str, size: int, permanent: bool = True) -> bool:
        """Creates a swapfile

        Args:
            location: The location of the swapfile
            size: The size of the swapfile
            permanent: True if permanent

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        def run_command(command):

            output = ftl.run_module_sync(
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
                loop=self.state["loop"],
                use_gate=self.state["gate"],
            )

            display_results(output, self.state["console"], self.state["log"])

        run_command(
            f"dd if=/dev/zero of={location} bs={size} count={int(size * 1024)} &&"
            f"chmod 600 {location} &&"
            f"mkswap {location} &&"
            f"swapon {location}"
        )

        return True

    description, inputs, output_type = get_json_schema(forward)


class Chown(Tool):
    name = "chown_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, user: str, location: str) -> bool:
        """Changes the ownership of a directory and the files in it.

        Args:
            location: The location of the swapfile
            user: The new owner of the location

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"chown -R {user} {location}",
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Chmod(Tool):
    name = "chmod_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, permissions: str, location: str) -> bool:
        """Changes the permissions of a file or directory.

        Args:
            location: The location of the swapfile
            permissions: The size of the swapfile

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"chmod {permissions} {location}",
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Mkdir(Tool):
    name = "mkdir_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str) -> bool:
        """Make a directory on the remote machine

        Args:
            name: The name of the directory

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        ftl.mkdir_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            name=name,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Copy(Tool):
    name = "copy_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Copy file to remote machine

        Args:
            src: The source of the file
            dest: The destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        ftl.copy_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            src=src,
            dest=dest,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class CopyFrom(Tool):
    name = "copy_from_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Copy file from remote machine locally

        Args:
            src: The remote source of the file
            dest: The local destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        ftl.copy_from_sync(
            self.state["inventory"],
            self.state["gate_cache"],
            src=src,
            dest=dest,
            loop=self.state["loop"],
        )

        display_results({}, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class SystemDService(Tool):
    name = "systemd_service_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str = "started", enabled: bool = False) -> bool:
        """Control systemd services

        Args:
            name: the name of the service
            state: one of reloaded, restarted, started, or stopped
            enabled: start on boot

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "systemd_service",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state, enabled=enabled),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class GetURL(Tool):
    name = "get_url_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, url: str, dest: str) -> bool:
        """Downloads a file

        Args:
            url: The url of the file
            dest: the destination of the file

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "get_url",
            self.state["gate_cache"],
            module_args=dict(
                url=url,
                dest=dest,
            ),
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Pip(Tool):
    name = "pip_tool"
    module = "pip"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, name: str, state: str = "present") -> bool:
        """Install python packages using pip

        Args:
            name: the name of the package
            state: one of latest, present, absent

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "pip",
            self.state["gate_cache"],
            module_args=dict(name=name, state=state),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class PipRequirements(Tool):
    name = "pip_requirements_tool"
    module = "pip"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, requirements: str, venv: str) -> bool:
        """Install dependencies from python requirements.txt files using pip.

        Args:
            requirements: the path to the requirements.txt file
            venv: the path to the virtual environment to install the packages to

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "pip",
            self.state["gate_cache"],
            module_args=dict(requirements=requirements, virtualenv=venv, virtualenv_command="python3 -m venv"),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Unarchive(Tool):
    name = "unarchive_tool"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, src: str, dest: str) -> bool:
        """Unarchives files from the archive file to the destination directory.

        Args:
            src: the name of the archive
            dest: the destination of the unarchived files

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "unarchive",
            self.state["gate_cache"],
            module_args=dict(src=src, dest=dest, remote_src=True),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class JavaJar(Tool):
    name = "java_jar_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, jar: str, args: list) -> bool:
        """Run a java jar

        Args:
            jar: the path of the jar file
            args: other arguments to the jar

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True,
                _raw_params=f"java -jar {jar} {' '.join(args)}",
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

        return True

    description, inputs, output_type = get_json_schema(forward)


class Bash(Tool):
    name = "bash_tool"
    module = "command"

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(self, script: str, user: str) -> bool:
        """Run a bash script

        Args:
            script: the path of the script to run
            user: the user to run the scrip as

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        output = ftl.run_module_sync(
            self.state["inventory"],
            self.state["modules"],
            "command",
            self.state["gate_cache"],
            module_args=dict(
                _uses_shell=True, _raw_params=f"sudo -u {user} bash {script}"
            ),
            dependencies=dependencies,
            loop=self.state["loop"],
            use_gate=self.state["gate"],
        )

        display_results(output, self.state["console"], self.state["log"])

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
    "Chmod",
    "Copy",
    "CopyFrom",
    "SystemDService",
    "GetURL",
    "Pip",
    "PipRequirements",
    "Unarchive",
    "Mkdir",
    "JavaJar",
    "Bash",
    "Timezone",
    "Git",
    "PodmanPull",
    "PodmanVersion",
    "PodmanRun",
]
